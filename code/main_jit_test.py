from main import main
from numba import jit


@jit()
def main_helper():
    main()


if __name__ == '__main__':
    main_helper()
