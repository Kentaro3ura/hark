# -*- coding: utf-8 -*-
import sys
import time
import numpy

verbose = False
if verbose:
    def verboseprint(*args):
        for arg in args:
           print arg,
        print
else:   
    verboseprint = lambda *a: None


# 重複判定の基準
MIN_INTERVAL = 0.5 # seconds


def evaluate(nPlayer, proc):
    print 'Start Judge!!'
    gnocchiTime = [0] * (nPlayer + 1)   # player + 1(speaker)
    start = time.time()
    while True:
        line = proc.stdout.readline()
        if not line and proc.poll() is not None:
            break
        line = line.rstrip('\r\n')

        # ログ出力フォーマット
        """
        time: 150, ID: 0, x: 0.000000e+000 1.000000e+000 6.000000e-001, power: 3.315118e+001, ID: 1, x: 9.960000e-001 -8.700000e-002 6.000000e-001, power: 3.301405e+001,
        time: 151, ID: 0, x: 0.000000e+000 1.000000e+000 6.000000e-001, power: 3.315118e+001, ID: 1, x: 9.960000e-001 -8.700000e-002 6.000000e-001, power: 3.301405e+001,
        """

        # 音源の入っていない情報は無視
        if len(line) < 80:
            continue
        # "time: " で始まるデータ以外は無視
        if line[0:5] != 'time:':
            continue
        data = line.split(',')
        j = 1
        while len(data) > j + 2:
            id_no = data[j][5:]
            xyz = data[j + 1][4:]
            j += 3
            x = float(xyz.split(' ')[0])
            y = float(xyz.split(' ')[1])
            theta = numpy.rad2deg(numpy.arctan2(y, x))
            # speaker(No.0) (-30 : 30)
            # No.1           (30 : 90)
            # No.2           (90 : 150)
            # No.3           (150 : 180), (-150 : -180)
            # No.4           (-90 : -150)
            # No.5           (-30 : -90)
            if -90.0 < theta <= -30.0:
                player = 1
            elif -150.0 < theta <= -90.0:
                player = 2
            elif -180.0 < theta <= -150.0 or 150.0 < theta <= 180.0:
                player = 3
            elif 90.0 < theta <= 150.0:
                player = 4
            elif 30.0 < theta <= 90.0:
                player = 5
            else:
                player = 0
            # print 'debug: id={0} theta={1} player={2}'.format(id_no, theta, player)

            gnocchiPlayer = player



            # 発話時刻を取得
            curr = time.time()
            verboseprint(gnocchiPlayer, curr)

            # 誤検知を防ぐために発話してから一定時間経過したプレーヤーを「成功」として扱い、
            # その音源からの発話を無視する
            # 成功者はgnocchiTimeにNoneをセットする(初期値はゼロ)
            for i, g in enumerate(gnocchiTime):
                # speakerの判定はスキップ
                if i == 0:
                    continue
                if g is not None and g != 0 and (curr - g) >= MIN_INTERVAL:
                    print 'PLAYER {0} SUCCEED!!'.format(i)
                    gnocchiTime[i] = None

            # 発話者がまだ成功していない場合は発話の重複をチェック
            if gnocchiTime[gnocchiPlayer] is not None:
                # 直前の発話から一定時間以内で重複とみなす
                for i, g in enumerate(gnocchiTime):
                    if i == gnocchiPlayer:
                        continue
                    if g is not None and (curr - g) < MIN_INTERVAL:
                        return [i, gnocchiPlayer]

                # 発話時刻を登録
                gnocchiTime[gnocchiPlayer] = curr

            # 残り一人かどうかをチェック
            playing_player_count = 0
            candidate_loser = 0
            for i, g in enumerate(gnocchiTime):
                # スピーカーはスキップ
                if i == 0:
                    continue
                if g is not None:
                    playing_player_count += 1
                    candidate_loser = i
            if playing_player_count == 1:
                return [candidate_loser]


if __name__ == '__main__':
    losePlayers = evaluate(5)
    print 'player ' + ' and '.join(map(str, losePlayers)) + ' lost'
