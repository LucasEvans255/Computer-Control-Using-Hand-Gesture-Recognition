from camera import Camera
import time


def main():
    cam = Camera(1280, 720)
    fps = []

    for i in range(300):
        print(f'At test{i}')

        start = time.perf_counter()
        n = 0
        for j in range(150):
            n += 1
            cam.grab_frame()
        dur = time.perf_counter() - start
        fps.append(n / dur)
        print(n / dur)
    
    print(f'Mean FPS: {sum(fps) / len(fps)}')


if __name__ == '__main__':
    main()
    