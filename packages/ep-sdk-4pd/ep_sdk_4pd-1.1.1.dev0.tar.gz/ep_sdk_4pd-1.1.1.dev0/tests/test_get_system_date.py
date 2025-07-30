from ep_sdk_4pd.ep_system import EpSystem


def test_get_system_date():
    print('-------------test_get_system_date-------------')

    target_date = EpSystem.get_system_date()
    print(target_date)
    print('-------------------------------------')


if __name__ == '__main__':
    test_get_system_date()
