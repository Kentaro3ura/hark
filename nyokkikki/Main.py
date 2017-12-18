#!/usr/bin/env python
# -*- coding: utf-8 -*-

import evaluate
import os
import random
import subprocess
import threading
import time
import winsound


NYOKKI_WAVS = [
    "sound/nyokki1.wav",
    "sound/nyokki2.wav",
    "sound/nyokki3.wav"
]

NUMBER_FILE = [
    "sound/No1.wav",
    "sound/No2.wav",
    "sound/No3.wav",
    "sound/No4.wav",
    "sound/No5.wav"
]


class HarkGame(object):
    def __init__(self):
        pass

    def _sound_file(self, file_name):
        winsound.PlaySound(file_name, winsound.SND_FILENAME)

    def _start_hark_nyokki(self):
        # 開始のかけ声
        time.sleep(random.randint(1, 4))
        self._sound_file(random.choice(NYOKKI_WAVS))

    def start_game(self):
        # 挨拶
        # time.sleep(1)
        # self._sound_file("sound/initiation.wav")
        #
        # # 開始の通知
        # time.sleep(1)
        # self._sound_file("sound/start.wav")
        # self._sound_file("sound/dondonpafupafu1.wav")

        # Harkの実行
        proc = subprocess.Popen('batchflow test.n', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        # ランダムな間をつくって開始の掛け声
        th_me = threading.Thread(target=self._start_hark_nyokki())
        th_me.start()

        # 判定処理呼び出し
        losers = evaluate.evaluate(5, proc)
        print 'losers={0}'.format(losers)
        proc.kill()

        # ゲーム終了の合図
        self._sound_file("sound/incorrect1.wav")

        # 結果報告
        is_first = True
        for loser in losers:
            if loser == 0:
                # chairmanの発話なのでスキップ
                continue
            if not is_first:
                self._sound_file("sound/to.wav")
            self._sound_file(NUMBER_FILE[loser - 1])
            is_first = False
        self._sound_file("sound/isLose.wav")

        # ゲーム終了通知
        time.sleep(1)
        self._sound_file("sound/end.wav")


if __name__ == '__main__':
    hark_game = HarkGame()
    hark_game.start_game()

