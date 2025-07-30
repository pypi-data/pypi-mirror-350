from ep_sdk_4pd.ep_data import EpData


def test_history_data():
    print('-------------test_history_data-------------')

    data = EpData.get_history_data(scope="market",days=1)
    # print(data)
    market = data.get("market")
    for m in market:
        print(m.get("day_ahead_tieline_power"))
    print('-------------------------------------')


if __name__ == '__main__':
    test_history_data()
