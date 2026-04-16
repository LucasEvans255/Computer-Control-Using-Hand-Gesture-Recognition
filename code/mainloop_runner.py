import multiprocessing
import tkinter as tk
from camera import Camera
from hand_finder import HandFinder
from model import Model
from commander import Commander


def cam_func(width: int, height: int, out_queue: multiprocessing.Queue):
    """
    Function for the process that runs the Camera
    """
    cam = Camera(width, height)

    while True:
        frame, stop = cam.grab_frame()

        out_queue.put((frame, stop))

        if stop == 1 or stop == 2:
            break


def handfinder_func(width: int, height: int, in_queue: multiprocessing.Queue, out_queue: multiprocessing.Queue):
    """
    Function for the process that runs the HandFinder
    """
    hands = HandFinder(width, height)

    while True:
        data = in_queue.get()

        if data[-1] == 1 or data[-1] == 2:
            # landmarks, hand, c_x, c_y, stop
            out_queue.put(([0 for _ in range(42)], 0, 0, 0, data[-1]))
            break
        
        data = hands.find(*data)
        out_queue.put(data)


def model_func(device: str, output_size: int, path: str, in_queue: multiprocessing.Queue, out_queue: multiprocessing.Queue):
    """
    Function for the process that runs the Model
    """
    model = Model(device, output_size, path)

    while True:
        landmarks, hand, c_x, c_y, stop = in_queue.get()

        if stop == 1 or stop == 2:
            out_queue.put((0, (0, 0), stop))
            break
        
        # If no hands have been detected, then this wont run and nothing will be placed in the queue
        if landmarks is not None:
            data = model.predict(landmarks, [c_x, c_y], stop)
            
            out_queue.put(data)

def commander_func(width: int, height: int, config_path: str, in_queue: multiprocessing.Queue):
    """
    Function for the process that runs the Commander
    """
    com = Commander(width, height, config_path)

    while True:
        label, centroid, stop = in_queue.get()

        if stop == 1:
            break
        if stop == 2:
            break
        com.run(label, centroid)

def error_window():
    """
    Reports to the user when there is an issue with connecting to the webcam
    """
    root = tk.Tk()
    root.geometry = "420x360"

    l1 = tk.Label(root, text="There was an error running the program.")
    l1.pack()
    l2 = tk.Label(root, text="Try checking your webcam is plugged in")
    l2.pack()

    root.mainloop()


class MainloopRunner:

    def __init__(self, width: int, height: int, device: str, output_size: int, path: str, config_path: str):
        """
        Class that runs the main loop of the program, i.e. grabbing frames -> executing commands and moving the mouse
        Width: int is the width of the webcam
        Height: int is the the height of the webcam
        Device: str is what device the neural network will be run on ('cuda' or 'cpu')
        Ouput_size: int is how many different gestures hte neural network has to predict from
        Path: str is for the Model object, and is the path to the csv file where the training data is stored
        Config_path: str is path to the config
        """
        self.q0 = multiprocessing.Queue()
        self.q1 = multiprocessing.Queue()
        self.q2 = multiprocessing.Queue()

        self.thread0 = multiprocessing.Process(target=cam_func, args=(width, height, self.q0,))
        self.thread1 = multiprocessing.Process(target=handfinder_func, args=(width, height, self.q0, self.q1,))
        self.thread2 = multiprocessing.Process(target=model_func, args=(device, output_size, path, self.q1, self.q2,))
        self.thread3 = multiprocessing.Process(target=commander_func, args=(width, height, config_path, self.q2,))

    def run(self) -> None:
        """
        Runs the mainloop by starting all the 4 threads used in the loop
        """
        self.thread0.start()
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()
