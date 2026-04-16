import cv2 as cv
from tkinter import ttk
from camera import Camera
from hand_finder import HandFinder
from model import Model
from config import Config
from mainloop_runner import error_window


class GestureAdder:

    def __init__(self, label_to_str: Config, bar: ttk.Progressbar, label: str, width: int, height: int, device: str, path: str):
        """
        Class that contains the code for allowin ghte user to add new gestures
        label_to_str is the integer label to string mapping config file
        bar is the bar that will be updated during retraining
        label is the string the user has inputted to identify the getsture
        width is the width of the webcam
        height is the height of the webcam
        device is the device the model will be run on 
        path is the path to the csv file
        """
        self.label = label
        self.label_to_str = label_to_str

        max_int = max([int(key) for key in self.label_to_str.json_dict.keys()])
        self.label_int = max_int + 1
        self.label_to_str.json_dict[str(self.label_int)] = self.label
        self.label_to_str.save()

        self.bar = bar

        self.cam = Camera(width, height)
        self.hands = HandFinder(width, height)
        self.model = Model(device, self.label_int, path)
        self.handle = self.model.handle

    def run(self):
        """
        Runs the program that allows the user to add new gestures
        Press 'enter' to take a photo, and the hand data will be added to the csv file
        When 250 of each hand are taken, it will retrain the model
        """
        right_count = 0
        left_count = 0

        while right_count < 251 or left_count < 251:
            frame, stop = self.cam.grab_frame()

            if stop == 2:
                error_window()
                break

            if cv.waitKey(1) == 13: # Code for 'enter'
                landmarks, hand, c_x, c_y, stop = self.hands.find(frame, stop)

                # Only run if the count for the given hand is less than 500 to avoid skewing the data with too much of one hand
                # The statement in the XOR for the hand that isnt detected is automatically false
                # So it will only run if the hand found has less than 500 already taken
                # if landmarks is not None and ((hand == 1 and right_count < 500) ^ (hand == 0 and left_count < 500)):
                if landmarks is not None:
                    if (hand == 1 and right_count < 251) ^ (hand == 0 and left_count < 251):
                        # If hand is 1 (right): r +=1, l += 0
                        # If hand is 0 (left): r += 0, l += 1
                        # This can be rewritten as r += hand, l += not hand
                        right_count += hand
                        left_count += int(not hand)

                        self.handle.add_row(self.label_int, hand, landmarks.tolist())
            
            font = cv.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            colour = (0, 255, 0)
            thickness = 2
            linetype = cv.LINE_AA
            frame = cv.putText(frame, f'Left count: {left_count}', (10, 25), font, font_scale, colour, thickness, linetype)
            frame = cv.putText(frame, f'Right count: {right_count}', (10, 70), font, font_scale, colour, thickness, linetype)
            cv.imshow(f'Adding gesture {self.label}', frame)
        
        self.model.retrain(self.bar)
