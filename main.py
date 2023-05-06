
# importar o tkinter para pegar os dados do CTRL+C sem baixar mais nada
from tkinter import Tk, TclError

import threading

# pra instalar o pyautogui se n tiver
import subprocess
import sys

# importa pyautogui, se n tiver baixa dai importa
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

        self.main()

    def get_clipboard(self):
        try:
            contents = Tk().clipboard_get().strip().replace('   ', '')
        except TclError:
            contents = ''
            
        return contents

    def paste(self, words: str):
        modules['pyautogui'].typewrite(words)
        
    def on_key_press(self, event):
        if event.name == self.key and event.event_type == 'down' and not self.latch:
            self.latch = True
            self.paste(self.get_clipboard())
        
        elif event.name == 'esc' and event.event_type == 'down':
            self.should_exit = True

    def on_key_release(self, event):
        if event.name == self.key and event.event_type == 'up' and self.latch:
            self.latch = False

    def listen_for_exit(self):
        modules['keyboard'].wait("esc")
        self.should_exit = True

    def main(self):
        # start a separate thread to listen for the "esc" key press event
        listener_thread = threading.Thread(target=self.listen_for_exit)
        listener_thread.start()

        # register key press and release event handlers
        modules['keyboard'].on_press_key(self.key, self.on_key_press)
        modules['keyboard'].on_release_key(self.key, self.on_key_release)
        

        # wait for exit (busy wait)
        while not self.should_exit:
            pass
        
        # exit the program
        exit()
    
if __name__ == '__main__':
    cliboard = ClipBoard()



