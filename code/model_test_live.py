import cv2 as cv
from camera import Camera
from hand_finder import HandFinder
from model import Model


def main():
    cam = Camera(1280, 720)
    finder = HandFinder(1280, 720)
    model = Model('cuda', 7, '.\\data.csv')

    label_to_str = {0: 'Point', 1: 'Fist', 2: 'Thumbs up', 3: 'Peace sign', 4: 'All fingers', 5: 'Thumb and index', 6: 'Thumb and 2 finger'}

    while True:
        frame, stop = cam.grab_frame()
        landmarks, hand, c_x, c_y, stop = finder.find(frame, stop)
        if landmarks is not None:
            label, centroid, stop = model.predict(landmarks, (c_x, c_y), stop)

            label_str = label_to_str[label]

            frame = cv.putText(frame, f'{label_str}', (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv.LINE_AA)

        if cv.waitKey(1) & 0xFF == 27:
            break

        cv.imshow('test', frame)

if __name__  == '__main__':
    main()
