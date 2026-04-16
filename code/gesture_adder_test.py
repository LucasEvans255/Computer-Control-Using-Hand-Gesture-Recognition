from gesture_adder import GestureAdder
from config import Config
import tkinter as tk
from tkinter import ttk
import threading


LABEL = 'Rock'
PATH = '.\\data_2_copy.csv'


def helper(bar: ttk.Progressbar):
    config = Config()
    config.load('.\\label_to_str.json')
    
    print('Making object')
    adder = GestureAdder(config, bar, LABEL, 1280, 720, 'cuda', PATH)
    print('Object initialised, running')
    adder.run()


def func(bar: ttk.Progressbar):
    thread = threading.Thread(target=helper, args=(bar,))
    thread.start()


def main():
    root = tk.Tk()

    bar = ttk.Progressbar(root)
    bar.pack()

    b = tk.Button(root, text='Add gesture', command=lambda: func(bar))
    b.pack()

    root.mainloop()

if __name__ == '__main__':
    main()
