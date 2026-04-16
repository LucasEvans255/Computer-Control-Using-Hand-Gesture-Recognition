import pyautogui
import threading
from funcs import *
from config import Config
from typing import Callable


class Commander:

    def __init__(self, width: int, height: int, config_path: str):
        """
        A class whose purpose is to encapsulate all of the interaction with the computer
        Controls moving the mouse and executing gestures
        Width and height are the width and height of the webcam
        """
        self.width = width
        self.height = height
        # Fill with -1 as -1 wont be assigned to any gesture
        self._gesture_queue = [-1 for _ in range(11)]
        self._label_to_func = _str_to_func(config_path)
    
    def _move_mouse(self, centroid: list[int, int]) -> None:
        """
        Moves the mouse to the X and Y coordinate determined by the centroid
        """
        x, y = centroid

        x = self._calc_coord(x, 'x')
        y = self._calc_coord(y, 'y')

        pyautogui.moveTo(x, y)

    def _calc_coord(self, coord: int, type: str):
        """
        Converts the coordinate from in the webcam space to the equivalent in the screen space
        Cuts off 15% from the sides in order to make it easier to move the mouse to the extremites of the screen
        """
        if type == 'x':
            webcam_dim = self.width
            screen_dim = pyautogui.size()[0]
        else:
            webcam_dim = self.height
            screen_dim = pyautogui.size()[1]
        
        # Cut off 15% from the sides
        coord = max(coord, 0.15 * webcam_dim)
        coord = min(coord, 0.85 * webcam_dim)

        # Convert the origin from (0.15 * webcam_x, 0.15 * webcam_y) to (0, 0)
        coord -= 0.15 * webcam_dim
        # Normalise to between 0 and 1
        coord /= 0.7 * webcam_dim

        coord = int(coord * screen_dim)
        return coord
    
    def _execute_gesture(self, label: int) -> None:
        """
        Executes a gesture given the label prediction
        Only executes a gesture when it has been held for exactly 10 frames
        """
        self._gesture_queue.pop(0)
        self._gesture_queue.append(label)

        valid = True

        # The first element in the queue cannot be same as the other 10, to ensure it only gets executed once after the first 10 frames
        if self._gesture_queue[0] == self._gesture_queue[1]:
            valid = False
            return

        for i in range(2, len(self._gesture_queue)):
            if self._gesture_queue[i] != self._gesture_queue[i - 1]:
                valid = False
                return
        
        if valid:
            self._label_to_func[label]()
        
    def run(self, label: int, centroid: list[int, int]) -> None:
        """
        Takes the label and centroid information
        Moves the mouse to the new coordinate
        Executes the gesture if it has been held for exactly 10 frames
        """
        move_thread = threading.Thread(target=self._move_mouse, args=(centroid,))
        execute_thread = threading.Thread(target=self._execute_gesture, args=(label,))
        move_thread.start()
        execute_thread.start()


def osk():
    pyautogui.hotkey('win', 'ctrl', 'o')

def none():
    pass

def _str_to_func(config_path: str) -> dict[int: Callable]:
        """
        Maps using the label_to_str.json file
        label_to_str contains an integer to string mapping, and this method contains a string to function mapping
        This is converted into an integer to function mapping, which is what is returned
        """
        config = Config()
        config.load(config_path)

        label_to_str = config.json_dict['label_to_button']

        label_to_func = {}

        # Functions that the user can assign to a gesture
        # left, right, double and middle click are implemented using their respective pyautgui functions
        # Opening an on screen keyboard has its own function
        # Keyboard keys to be used using pyautogui: nexttrack, prevtrack, printscr, windows, delete, browserback, browserforward, browserrefresh, pageup, pagedown, volumeup, volumedown, volumemute
        # Also have a None function if the user wants a gesture that wont execute anything

        for label in label_to_str:
            label_to_func[int(label)] = func_from_str(label_to_str[label])
        
        return label_to_func
