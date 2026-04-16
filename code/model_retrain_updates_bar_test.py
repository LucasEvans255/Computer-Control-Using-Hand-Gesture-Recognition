import tkinter as tk
import threading
from tkinter import ttk
from model import Model
from csv_handle import csvHandle


def retrain_helper(bar, n):
    model = Model('cuda', n, '.\\data.csv')
    model.retrain(bar)


def retrain(bar, n):
    t = threading.Thread(target=retrain_helper, args=(bar, n))
    t.start()


def main():
    root = tk.Tk()

    bar = ttk.Progressbar(root)
    bar.pack()

    handle = csvHandle('.\\data.csv')
    n = handle.count_labels()

    b = tk.Button(root, command=lambda: retrain(bar, n))
    b.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
