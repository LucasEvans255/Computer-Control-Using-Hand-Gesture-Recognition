import cv2 as cv
import numpy as np
from win32api import GetKeyState


class Camera:

    def __init__(self, width: int, height: int):
        """
        Initialises a class that acts as a wrapper around an opencv VideoCapture object
        The width and height parameters will be set as the width and height dimensions that frames are grabbed at
        """
        self.cam = cv.VideoCapture(0)
        self.width = width
        self.height = height

        # 3 corresponds to width, 4 corresponds to height
        self.cam.set(3, int(self.width))
        self.cam.set(4, int(self.height))

    def grab_frame(self) -> tuple[np.ndarray[np.ndarray[np.uint8]], int]:
        """
        Grabs a frame from the user's webcam
        If the user presses 'esc', the value of integer returned will be 1
        If the camera fails to initialise or a frame cannot be grabbed it will return 2
        A return value of 0 indicates that it is okay to continue
        """
        ret, frame = self.cam.read()
        stop = 0

        # 27 is the UTF-8 code for 'esc'
        key = GetKeyState(27)
        if key == -127 or key == -128:
            stop = 1
        elif ret == False:
            stop = 2

        return frame, stop

