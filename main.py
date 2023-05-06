from tkinter import Tk, TclError
import subprocess
import sys
import multiprocessing as mp

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
        if event.name == self.key and event.event_type == 'down' and not self.latch:
            self.latch = True

            paste_process = mp.Process(target=self.paste, args=(self.get_clipboard(),))
            paste_process.start()
        
        elif event.name == 'esc' and event.event_type == 'down':
            self.should_exit = True

    def on_key_release(self, event):
        if event.name == self.key and event.event_type == 'up' and self.latch:
            self.latch = False

    def listen_for_exit(self, should_exit):
        modules['keyboard'].wait("esc")
        should_exit.value = True

    def main(self, should_exit):
        # start a separate process to listen for the "esc" key press event
        listener_process = mp.Process(target=self.listen_for_exit, args=(should_exit,))
        listener_process.start()

        # register key press and release event handlers
        modules['keyboard'].on_press_key(self.key, self.on_key_press)
        modules['keyboard'].on_release_key(self.key, self.on_key_release)
        
        print('Running... >> PRESSIONE ESC PARA PARAR O PROGRAMA <<')
        # wait for exit (busy wait)
        while True:
            if should_exit.value:
                print('Quitting...')
                exit()
    
    
if __name__ == '__main__':
    should_exit = mp.Value('b', False)
    cliboard = ClipBoard()
    cliboard.main(should_exit)
    print('YEP')
