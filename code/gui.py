import tkinter as tk
import multiprocessing
import threading
import shutil
import os
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
from config import Config
from mainloop_runner import MainloopRunner
from gesture_adder import GestureAdder


class GUI:

    def __init__(self):
        """
        Initialising this object runs the whole app
        """
        self.root = tk.Tk()

        self._save_config_as_button = tk.Button(self.root, text='Save config as', width=22, height=2, command=self.save_config_as)
        self._save_config_as_button.grid(row=0, column=0)

        self._load_config_as_button = tk.Button(self.root, text='Load config', width=22, height=2, command=self.load_config)
        self._load_config_as_button.grid(row=0, column=1)

        self._edit_config_button = tk.Button(self.root, text='Edit config', width=22, height=2, command=self.edit_config)
        self._edit_config_button.grid(row=0, column=2)

        self._help_button = tk.Button(self.root, text='Help', width=10, height=2, command=self.help)
        self._help_button.grid(row=0, column=5, padx=(75, 0))

        self._start_button = tk.Button(self.root, text='Start program', width=15, height=5, command=self.start)
        self._start_button.grid(row=3, column=1, padx=40, pady=50)

        self._add_new_gesture_button = tk.Button(self.root, text='Add new gesture', width=15, height=5, command=self.add_new_gesture)
        self._add_new_gesture_button.grid(row=3, column=3, padx=40, pady=50)

        self._reset_button = tk.Button(self.root, text='Reset', width=10, height=2, command=self.reset)
        self._reset_button.grid(row=5, column=5, padx=(75, 0))

        self._config_path = open('.\\config_path.txt', 'r').read()

        self.label_to_str = Config()
        self.label_to_str.load('.\\label_to_str.json')

        self.config = Config()
        self.config.load(self._config_path)

        self.root.mainloop()

    def save_config_as(self):
        """
        Asks for a string from the user that will be the filename
        .\\ is added to the beginning of the string to make sure it is saved in the main directory
        .json is added to the end to make sure it is saved a .json file
        The config_path.txt file is also updated appropriately
        """
        path = '.\\' + simpledialog.askstring('Save config as', 'Enter filename (.json will be added to the end)') + '.json'

        self.config.save_as(path)
        self._config_path = path

        with open('.\\config_path.txt', 'w') as f:
            f.write(path)
    
    def load_config(self):
        """
        Opens a file explorer window where the user has to open a config file
        If the file is not valid, nothing happens
        """
        path = filedialog.askopenfilename()

        success = self.config.load(path)
        if success == 2:
            self._config_path = path
            with open('.\\config_path.txt', 'w') as f:
                f.write(path)
    
    def start(self):
        """
        Starts the main loop of the program
        """
        width = int(self.config.json_dict['cam_width'])
        height = int(self.config.json_dict['cam_height'])
        device = self.config.json_dict['device']
        # Has to add one as the keys as 0-indexed, so if there are 7 outputs, the max key is only 6
        output_size = max([int(key) for key in self.label_to_str.json_dict.keys()]) + 1
        path = '.\\data.csv'

        info_win = tk.Tk()
        l1 = tk.Label(info_win, text="Program starting. Press 'esc' on\n the keyboard, or bind a gesture\n to 'esc',to close the application")
        l1.grid(row=0, column=0)

        # Has to be spawned in its own process otherwise the tkinter mainloop will prevent it from running
        p = multiprocessing.Process(target=run_mainloop, args=(width, height, device, output_size, path, self._config_path, ))
        p.start()

        info_win.mainloop()
    
    def add_new_gesture(self):
        """
        Asks the user for a string which will be the label for the new gesture
        Then runs the code for adding a gesture
        Also opens a tkinter window with a progress bar that indicates how far along the NN is in training after the data has been gathered
        """
        label = simpledialog.askstring('Add new gesture', 'Enter name of new gesture')

        if label is not None:
            progress_win = tk.Tk()
            l = tk.Label(progress_win, text='Retraining. Do not close this window')
            l.grid(row=0, column=0)

            bar_step = tk.IntVar()
            bar_step.set(0)
            bar = ttk.Progressbar(progress_win, variable=bar_step)
            bar.grid(row=1, column=0)

            width = self.config.json_dict['cam_width']
            height = self.config.json_dict['cam_height']
            device = self.config.json_dict['device']
            path = '.\\data.csv'

            # These have to be threads not processes, as launching a process requires pickling all the args
            # Unfortunately both tkinter objects and Config objects are not pickleable
            adder_thread = threading.Thread(target=adder_helper, args=(self.label_to_str, bar, label, width, height, device, path,), daemon=True)
            destroy_thread = threading.Thread(target=destroy_helper, args=(progress_win, bar, bar_step), daemon=True)
            adder_thread.start()
            destroy_thread.start()

            progress_win.mainloop()

    def reset(self):
        """
        Copys data from all the default files to the actual files
        Will delete any extra gestures that have been added
        """
        choice = messagebox.askokcancel('Reset', 'You are about to reset to default settings. Any extra gestures you have added will be deleted')
        if choice:
            shutil.copyfile('.\\default_data.csv', '.\\data.csv')
            shutil.copyfile('.\\default_label_to_str.json', '.\\label_to_str.json')
            shutil.copyfile('.\\default_config.json', '.\\config.json')
            with open('.\\config_path.txt', 'w') as f:
                f.write('.\\config.json')
            
            shutil.copyfile('.\\default_model.pickle', '.\\model.pickle')

    def edit_config(self):
        """
        Opens the window where the user can edit all the config files
        """
        # For some reason running this EXACT code in this file causes all the option menus to not fucking work for some nonsensical reason
        # It still "works" without doing this but the user cant see what they have selected or what the current values are
        # Which would ofc be really inconvenient 
        # For some reason this is the only way that error can be circumvented, so DONT CHANGE THIS
        os.system('python repo\\gui_run_edit_config.py')

    def help(self):
        """
        Opens word document guiding the user on how to use the program
        """
        os.system('.\\help.docx')


def run_mainloop(width: int, height: int, device: str, output_size: int, path: str, config_path: str):
    """
    Helper function that initialises a MainloopRunner object and runs it
    """
    runner = MainloopRunner(width, height, device, output_size, path, config_path)
    runner.run()

def adder_helper(label_to_str: Config, bar: ttk.Progressbar, label: str, width: int, height: int, device: str, path: str):
    """
    Helper function that initialises a GestureAdder object and runs it
    """
    adder = GestureAdder(label_to_str, bar, label, width, height, device, path)
    adder.run()

def destroy_helper(bar_win: tk.Tk, bar: ttk.Progressbar, step: tk.IntVar):
    """
    Helper function that checks the current step of the progress bar, and if it is completed, destroys the window to indicate to the user it is done
    """
    maximum_step = bar.config()['maximum'][-1] - 1
    while True:
        if step.get() == maximum_step:
            bar_win.destroy()
