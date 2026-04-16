import cv2 as cv
import numpy as np
from hand_finder import HandFinder
from camera import Camera


def main():
    cam = Camera(1280, 720)
    hands = HandFinder(1280, 720)

    while True:
        frame, stop = cam.grab_frame()

        if stop != 0:
            break

        prev_stop = stop

        landmarks, c_x, c_y, stop = hands.find(frame, stop)

        if landmarks is not None and c_x and c_y:
            assert(all([l >= 0 and l <= 1 for l in landmarks]))
            assert(stop == prev_stop)
            assert(len(landmarks.shape) == 1)
            assert(type(c_x) == int)
            assert(type(c_y) == int)

            frame = cv.circle(frame, (c_x, c_y), 15, (0, 255, 0), -1)

        cv.imshow('frame with detected centroid', frame)


if __name__ == '__main__':
    main()
