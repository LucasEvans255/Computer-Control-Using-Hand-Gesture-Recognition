from config import Config
from gui_edit_config import edit_config_win


def main():
    label_to_str = Config()
    label_to_str.load('.\\label_to_str.json')
    config = Config()
    config.load(open('.\\config_path.txt').read())
    edit_config_win(label_to_str, config)


if __name__ == '__main__':
    main()
