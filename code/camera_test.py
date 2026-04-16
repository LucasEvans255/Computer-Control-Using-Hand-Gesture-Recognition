from camera import Camera
import cv2 as cv


def main():
    cam = Camera(1280, 720)
    stop = 0

    while True:
        frame, stop = cam.grab_frame()

        if stop != 0:
            break

        cv.imshow('capture', frame)
    print(f'Stopped as stop returned value of: {stop}')


if __name__ == '__main__':
    main()
