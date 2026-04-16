import tkinter as tk
from tkinter import ttk


def main():
    root = tk.Tk()

    save_con_as_b = tk.Button(root, text='Save config as', width=22, height=2)
    save_con_as_b.grid(row=0, column=0)

    load_con_b = tk.Button(root, text='load config', width=22, height=2)
    load_con_b.grid(row=0, column=1)

    edit_con_b = tk.Button(root, text='Edit config', width=22, height=2)
    edit_con_b.grid(row=0, column=2)

    help_b = tk.Button(root, text='Help', width=10, height=2)
    help_b.grid(row=0, column=5, padx=(75, 0))

    start_b = tk.Button(root, text='Start program', width=15, height=5)
    start_b.grid(row=3, column=1, padx=40, pady=50)

    add_new_b = tk.Button(root, text='Add new gesture', width=15, height=5)
    add_new_b.grid(row=3, column=3, padx=40, pady=50)

    reset_b = tk.Button(root, text='Reset', width=10, height=2)
    reset_b.grid(row=5, column=5, padx=(75, 0))

    root.mainloop()


if __name__ == '__main__':
    main()
