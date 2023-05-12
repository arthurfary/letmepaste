import signal
from tkinter import Tk, TclError
import subprocess
import sys
import multiprocessing as mp
import os
from time import sleep

import_list = ['pyautogui', 'keyboard']
modules = {}
try:
    for import_var in import_list:
        modules[import_var] = __import__(import_var)

except ModuleNotFoundError:
    python = sys.executable

    for import_var in import_list:
        subprocess.check_call(
            [python, '-m', 'pip', 'install', import_var]
        )

finally:
    for import_var in import_list:
        modules[import_var] = __import__(import_var)


class ClipBoard:
    def __init__(self):
        self.key = 'right ctrl'
        self.latch = False
        self.should_exit = False

    def get_clipboard(self):
        try:
            tab = '\t'
            contents = Tk().clipboard_get().strip().replace(tab, '').replace('    ', '')
        except TclError:
            contents = ''

        print('contents:', contents)
        return contents

    def paste(self, words: str):
        modules['pyautogui'].write(words)

    def on_key_press(self, event):
        print(event.name)
        if event.name == self.key and event.event_type == 'down' and not self.latch:
            self.latch = True

            paste_process = mp.Process(target=self.paste, args=(self.get_clipboard(),))
            paste_process.start()


    def on_key_release(self, event):
        if event.name == self.key and event.event_type == 'up' and self.latch:
            self.latch = False



    def main(self):

        # register key press and release event handlers
        modules['keyboard'].on_press_key(self.key, self.on_key_press)
        modules['keyboard'].on_release_key(self.key, self.on_key_release)

        print('\n\nRunning...\n >> LEMBRE-SE DE FECHAR O PROGRAMA<<')
        modules['keyboard'].wait()









if __name__ == '__main__':
    should_exit = mp.Value('b', False)
    cliboard = ClipBoard()
    cliboard.main()
    print('Starting...')
