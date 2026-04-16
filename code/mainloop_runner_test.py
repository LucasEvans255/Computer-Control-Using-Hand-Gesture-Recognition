from mainloop_runner import MainloopRunner


def main():
    runner = MainloopRunner(1280, 720, 'cuda', 7, '.\\data_2.csv')
    runner.run()


if __name__ == '__main__':
    main()
