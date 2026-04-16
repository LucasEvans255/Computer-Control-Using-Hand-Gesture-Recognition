from config import Config


SOURCE = '.\\json_test_files\\'
V_CONFIG = SOURCE + 'valid_config.json'
INV_CONFIG_EXTRA = SOURCE + 'invalid_config_extra_field.json'
INV_CONFIG_MISSING = SOURCE + 'invalid_config_missing_field.json'
INV_CONFIG_STR_IN_LTB = SOURCE + 'invalid_config_str_in_ltb.json'
V_LTS = SOURCE + 'valid_label_to_str.json'
INV_LTS = SOURCE + 'invalid_label_to_str.json'
INV_NAME = SOURCE + 'valid_config.jso'


def main():
    config = Config()

    assert(config.load(V_CONFIG) == 2)
    assert(config.load(INV_CONFIG_EXTRA) == 0)
    assert(config.load(INV_CONFIG_MISSING) == 0)
    assert(config.load(INV_CONFIG_STR_IN_LTB) == 0)
    assert(config.load(V_LTS) == 1)
    assert(config.load(INV_LTS) == 0)
    assert(config.load(INV_NAME) == 0)

    print('All assertions passed')


if __name__ == '__main__':
    main()
