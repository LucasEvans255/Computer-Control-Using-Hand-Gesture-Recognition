from csv_handle import csvHandle
import pandas as pd
import random


PATH = '.\\test_data.csv'


def main():
    handle = csvHandle(PATH)
    df = pd.read_csv(PATH)
    print(df)
    n = len(df)

    data = [random.randint(0, 10)] + [random.choice([0, 1])] + [random.random() for _ in range(42)]
    handle.add_row(data[0], data[1], data[2:])

    print(pd.read_csv(PATH))
    assert(len(pd.read_csv(PATH)) == n + 1)


if __name__ == '__main__':
    main()
