import time
import cv2 as cv
from camera import Camera
from hand_finder import HandFinder
from model import Model
from commander import Commander


ITERS = 5_000


def main():
    cam = Camera(1280, 720)
    cam_times = []
    print("Testing camera")

    for i in range(1, ITERS + 1):
        if i % 100 == 0:
            print(f"At test: {i}")

        start = time.perf_counter()
        frame, stop = cam.grab_frame()
        dur = time.perf_counter() - start
        cam_times.append(dur)
    
    print("Testing HandFinder")
    hands = HandFinder(1280, 720)
    hands_times = []

    for i in range(1, ITERS + 1):
        if i % 100 == 0:
            print(f"At test: {i}")

        start = time.perf_counter()
        res = hands.find(frame, 0)
        dur = time.perf_counter() - start
        hands_times.append(dur)
    
    print("Testing model on CPU")
    model_cpu_times = []
    model = Model('cpu', 7, '.\\data.csv')

    for i in range(1, ITERS + 1):
        if i % 100 == 0:
            print(f"At test: {i}")

        start = time.perf_counter()
        model.predict(res[0], (res[2], res[3]), 0)
        dur = time.perf_counter() - start
        model_cpu_times.append(dur)
    
    print("Testing model on GPU")
    model_gpu_times = []
    model = Model('cuda', 7, '.\\data.csv')

    for i in range(1, ITERS + 1):
        if i % 100 == 0:
            print(f"At test: {i}")

        start = time.perf_counter()
        model.predict(res[0], (res[2], res[3]), 0)
        dur = time.perf_counter() - start
        model_gpu_times.append(dur)
    
    print("Testing commander")
    comm_times = []
    comm = Commander(1280, 720, '.\\config.json')

    for i in range(1, (ITERS // 10) + 1):
        if i % 10 == 0:
            print(f"At test: {i}")

        start = time.perf_counter()
        comm.run(0, [500, 200])
        dur = time.perf_counter() - start
        comm_times.append(dur)

        for j in range(10):
            start = time.perf_counter()
            comm.run(1, [500, 200])
            dur = time.perf_counter() - start
            comm_times.append(dur)
    
    print(f"Camera took on average {sum(cam_times) / len(cam_times)} seconds")
    print(f"HandFinder on average took {sum(hands_times) / len(hands_times)} seconds")
    print(f"Model on CPU on average took {sum(model_cpu_times) / len(model_cpu_times)} seconds")
    print(f"Model on GPU on average took {sum(model_gpu_times) / len(model_gpu_times)} seconds")
    print(f"Commander on average took {sum(comm_times) / len(comm_times)} seconds")


if __name__ == '__main__':
    main()
