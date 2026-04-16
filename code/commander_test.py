import time
from commander import Commander
from config import Config


def main():
    comm = Commander(1280, 720)
    con = Config()
    con.load('.\\label_to_str.json')

    for i in range(7):
        input(f"Press enter to test input {con.json_dict[str(i)]} 5 seconds from now")
        time.sleep(5)
        for j in range(20):
            comm.run(i, [500, 200])

if __name__ == '__main__':
    main()
