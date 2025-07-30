from ep_sdk_4pd.ep_system import EpSystem


def test_model_output_dir():
    print('-------------test_model_output_dir-------------')

    data = EpSystem.model_output_dir(is_online=True)
    print(data)
    print('-------------------------------------')


if __name__ == '__main__':
    test_model_output_dir()
