from camera import Camera
from hand_finder import HandFinder
import time
import cv2 as cv


def main():
    times = []
    cam = Camera(1280, 720)
    hands = HandFinder(1280, 720)

    for i in range(1_000):
        print(f'At test {i}')

        frame, stop  = cam.grab_frame()
        cv.imshow('test', frame)

        start = time.perf_counter()
        res = hands.find(frame, stop)
        end = time.perf_counter()
        times.append(end - start)
    
    print(f'On average detection took: {(sum(times) / len(times) * 1_000)} ms')

if __name__ == '__main__':
    main()
