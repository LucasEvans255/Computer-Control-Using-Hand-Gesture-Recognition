import numpy as np
import cv2 as cv
import mediapipe as mp
mp_hands = mp.solutions.hands

COMPLEXITY = 0


class HandFinder:

    def __init__(self, width: int, height: int):
        """
        This class contains all the functionality to locate hand landmarks and normalise them
        It contains a mediapipe hands object which is used for the location
        The width and height parameters are the width and height of the users webcam, and is used for the normalisation process
        """
        self.hands = mp_hands.Hands(model_complexity=COMPLEXITY, 
                                    min_detection_confidence=0.5,
                                    min_tracking_confidence=0.5)
        self.width = width
        self.height = height

    def find(self, frame: np.ndarray[np.ndarray[np.uint8]], stop: int) -> tuple[list[float], int, int, int, int]:
        """
        Locates hands within the frame
        Return the normalised landmarks, which hand is detected (0: left, 1: right), and the unnormalised centroid coordinates
        """
        # Gets the results from the hands ai
        frame = cv.flip(frame, 1)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.hands.process(frame)

        # Only runs if any hands are actually detected
        if results.multi_hand_landmarks:
            # Only uses data from the first hand detected to avoid issues with multiple hands
            points = results.multi_hand_landmarks[0]
            handedness = results.multi_handedness[0]
            hand = handedness.classification[0].index

            landmarks = []

            for point in points.landmark:
                # Converts the points from float values into integers for normalisation
                # Take the minimum in case any points are calculated to be outside the webcam's dimensions
                x = min(int(point.x * int(self.width)), int(self.width) - 1)
                y = min(int(point.y * int(self.height)), int(self.height) - 1)
                landmarks.append([x, y])
            
            norm_landmarks = self._normalise(landmarks)
            # This is the same effect as flattening the array
            # e.g. reshape([[1, 2], [3, 4]], -1) = [1, 2, 3, 4]
            norm_landmarks = np.reshape(norm_landmarks, -1)

            # The 9th element is the middle finger joint, which is chosen to represent the centre as it's location is least affected by finger movement
            centroid_x, centroid_y = landmarks[9]
        else:
            norm_landmarks = hand = centroid_x = centroid_y = None

        return norm_landmarks, hand, centroid_x, centroid_y, stop

    def _normalise(self, landmarks: list[list[int]]) -> np.ndarray[np.ndarray[float, float]]:
        """
        Custom normalisation routine for converting hand landmarks anywhere in the frame into float values between 0 and 1
        This ensures that the same gesture in a different part of the image will be represented by similar values
        e.g. without this process, the ai will see a gesture more to the right as different as it's x values will be higher
        Dry run to explain the process

        landmarks = [[1, 2], [2, 4], [5, 3], [3, 3]]
        x_min = 1
        x_max = 5
        y_min = 2
        y_max = 4

        subtract the minimum values:
        landmarks - [x_min, y_min] = [[0, 0], [1, 2], [4, 1], [2, 1]]

        multiply x values by 1 / (x_max - x_min) and y values by 1 / (y_max - x_min)
        1 / (x_max - x_min) = 1/4
        1 / (y_max - x_min) = 1/2
        landmarks = [[0, 0], [0.25, 1], [1, 0.5], [0.5, 0.5]]

        This process can be generally represented by these matrix operations:

        ||[x0, y0]  |   |[x_min, y_min]||
        ||[x1, y1]  |   |[x_min, y_min]||
        ||   .      |   |      .       ||   |[1 / (x_max - x_min), 0]|
        ||   .      | - |      .       || * |[0, 1 / (y_max - y_min)]|
        ||   .      |   |      .       ||
        ||[x40, y40]|   |[x_min, y_min]||
        ||[x41, y41]|   |[x_min, y_min]||

        (landmarks - [x_min, y_min]) * ([1 / (x_max - x_min), 0], [0, 1 / (y_max - y_min)])
        """
        x_max, y_max = np.max(landmarks, axis=0)
        x_min, y_min = np.min(landmarks, axis=0)

        scale_matrix = np.array([[1 / (x_max - x_min), 0], [0, 1 / (y_max - y_min)]])
        min_subtracted = np.array(landmarks) - [x_min, y_min]

        return np.matmul(min_subtracted, scale_matrix)
    