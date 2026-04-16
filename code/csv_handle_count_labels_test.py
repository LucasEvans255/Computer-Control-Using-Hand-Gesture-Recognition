import pandas as pd
from csv_handle import csvHandle


PATH = '.\\test_data.csv'


def main():
    handle = csvHandle(PATH)
    df = pd.read_csv(PATH)

    print(df['label'].values)
    print(handle.count_labels())


if __name__ == '__main__':
    main()
