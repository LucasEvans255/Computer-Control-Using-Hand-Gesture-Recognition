from camera import Camera
from hand_finder import HandFinder
from csv_handle import csvHandle
import numpy as np
import cv2 as cv
import random

# 0: point, 1: fist, 2: thumbs up, 3: peace sign, 4: all fingers, 5: thumb and finger, 6: thumb and 2 fingers
LABEL = 6


def main():
    cam = Camera(1280, 720)
    finder = HandFinder(1280, 720)
    handle = csvHandle('.\\data_2.csv')

    left_count = 0
    right_count = 0

    stop = 0

    while left_count < 251 or right_count < 251 and stop == 0:
        frame, stop = cam.grab_frame()

        if cv.waitKey(1) == 121:
            landmarks, hand, c_x, c_y, stop = finder.find(frame, stop)

            if landmarks is not None: #and ((hand == 0 and right_count < 251) ^ (hand == 1 and right_count < 251)):
                print('Running')
                if hand == 0:
                    left_count += 1
                else:
                    right_count += 1
                
                points = np.reshape(landmarks, (len(landmarks) // 2, 2))

                # x = random.random()

                # if 0 < x < 0.5:
                #     if 0 < x < 0.05:
                #         a = random.uniform(0.5 * np.pi, 1.5 * np.pi)
                #     else:
                #         a = random.uniform(-0.5 * np.pi, 0.5 * np.pi)
                #     rot = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
                #     new_points = np.matmul(rot, points.T).T
                #     new_landmarks = new_points.reshape(-1)
                #     new_data = new_landmarks.tolist()
                #     handle.add_row(LABEL, hand, new_data)
                
                handle.add_row(LABEL, hand, landmarks.tolist())

        cv.putText(frame, f'Left count: {left_count}', (10, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
        cv.putText(frame, f'Right count: {right_count}', (10, 600), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
        cv.imshow('data gathering', frame)


if __name__ == '__main__':
    main()
