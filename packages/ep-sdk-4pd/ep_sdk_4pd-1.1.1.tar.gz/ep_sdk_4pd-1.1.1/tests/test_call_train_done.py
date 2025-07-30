from ep_sdk_4pd.ep_system import EpSystem


def test_call_train_done():
    print('-------------test_call_train_done-------------')

    data = EpSystem.call_train_done(strategy_id=3,script_strategy_id=5)
    print(data)
    print('-------------------------------------')


if __name__ == '__main__':
    test_call_train_done()
