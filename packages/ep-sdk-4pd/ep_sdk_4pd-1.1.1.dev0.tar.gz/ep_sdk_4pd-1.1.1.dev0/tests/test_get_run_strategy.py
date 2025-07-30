from ep_sdk_4pd.ep_system import EpSystem


def test_get_run_strategy():
    print('-------------test_get_run_strategy-------------')

    data = EpSystem.get_run_strategy(is_online=True)
    print(data)
    print('-------------------------------------')


if __name__ == '__main__':
    test_get_run_strategy()
