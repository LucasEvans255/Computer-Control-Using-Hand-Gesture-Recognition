import torch
import tkinter as tk
import threading
from tkinter import ttk
from model import Model
from csv_handle import csvHandle


PATH = '.\\data.csv'


def retrain_helper(bar, n, root):
    model = Model('cuda', n, PATH)
    model.retrain(bar)
    root.destroy()


def retrain(bar, n, root):
    t = threading.Thread(target=retrain_helper, args=(bar, n, root))
    t.start()


def main_2():
    root = tk.Tk()

    bar = ttk.Progressbar(root)
    bar.pack()

    handle = csvHandle(PATH)
    n = handle.count_labels()

    b = tk.Button(root, command=lambda: retrain(bar, n, root))
    b.pack()

    root.mainloop()


def main():
    main_2()

    handle = csvHandle(PATH)
    n = handle.count_labels()
    model = Model('cuda',  n, PATH)

    X, Y = handle.prepare_data()

    accuracies = []
    
    for points, label in zip(X, Y):
        points = torch.tensor(points, dtype=torch.float, device='cuda')
        label = torch.tensor(label, dtype=torch.int64, device='cuda')
        Y_hat, centroid, stop = model.predict(points.tolist(), [0, 0], 0)
        accuracies.append(int(Y_hat == label))
    
    print(f'Accuracy: {sum(accuracies) / len(accuracies)}')
    exit()


if __name__ == '__main__':
    main()
