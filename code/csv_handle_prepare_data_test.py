import pandas as pd
from csv_handle import csvHandle


PATH = '.\\test_data.csv'


def main():
    df = pd.read_csv(PATH)
    print(df)
    handle = csvHandle(PATH)

    X, Y = handle.prepare_data()

    print(X)
    print(Y)

    assert len(df) == len(X)

if __name__ == '__main__':
    main()
