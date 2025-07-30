import json
from datetime import timedelta, datetime

import requests

from ep_sdk_4pd import models as ep_sdk_4pd_models
from ep_sdk_4pd.ep_system import EpSystem
from ep_sdk_4pd.models import HistoryDataRequest, PredictDataRequest

# test 地址
# endpoint = 'http://172.27.88.56:6001'

# prod 地址
# endpoint = 'http://172.27.88.56:6601'

# 外网 地址
endpoint = 'http://82.157.231.254:6001'

Authorization = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlbGVjdHJpY2l0eS1wbGF0Zm9ybSIsInN1YiI6IjEyMyIsImlhdCI6MTc0NjYwNjQ4NSwianRpIjoiMTIzXzE3NDY1Nzc2ODUxNDYiLCJ0eXBlIjoiYWNjZXNzIn0.Clrz_8j3aJlXTWPX-4DS0NxXN9idTcUIc0AtXOMIjd8'


class EpData:

    @staticmethod
    def get_history_data(
            scope="weather,plant,market",
            days=0
    ):
        # 最晚时间为系统时间 D-2
        date_str = EpSystem.get_system_date(is_online=True)
        calculated_date = datetime.strptime(date_str, "%Y-%m-%d")
        system_date = calculated_date.strftime("%Y-%m-%d")  # 转换回字符串

        request = HistoryDataRequest(
            scope=scope,
            system_date=system_date,
            days=days,
        )
        response = EpData.history_data(request=request)

        if response.code == 200:
            return response.data
        else:
            return None

    @staticmethod
    def history_data(
            request: ep_sdk_4pd_models.HistoryDataRequest = None,
    ) -> ep_sdk_4pd_models.HistoryDataResponse:

        full_url = f'{endpoint}{request.api}'
        headers = {
            'content-type': request.content_type,
            'Authorization': Authorization
        }

        payload = {
            'scope': request.scope,
            'system_date': request.system_date,
            'days': request.days
        }

        response = requests.request(
            method=request.method,
            url=full_url,
            headers=headers,
            data=json.dumps(payload),
        )

        base_resp = ep_sdk_4pd_models.BaseResponse(
            code=response.json().get('code', None),
            data=response.json().get('data', None),
            message=response.json().get('message', None),
        )
        return ep_sdk_4pd_models.HistoryDataResponse(response=base_resp)

    @staticmethod
    def get_predict_data(
            scope="weather,plant,market",
            is_test=False,
            test_time=None,
    ):
        date_str = EpSystem.get_system_date(is_online=True)
        calculated_date = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)  # 增加 +1 天
        system_date = calculated_date.strftime("%Y-%m-%d")

        # 测试
        # if is_test:
        #     system_date = test_time

        request = PredictDataRequest(
            scope=scope,
            system_date=system_date,
        )
        response = EpData.predict_data(request=request)

        if response.code == 200:
            return response.data
        else:
            return None

    @staticmethod
    def predict_data(
            request: ep_sdk_4pd_models.PredictDataRequest = None,
    ) -> ep_sdk_4pd_models.PredictDataResponse:

        full_url = f'{endpoint}{request.api}'
        headers = {
            'content-type': request.content_type,
            'Authorization': Authorization
        }

        payload = {
            'scope': request.scope,
            'system_date': request.system_date
        }

        response = requests.request(
            method=request.method,
            url=full_url,
            headers=headers,
            data=json.dumps(payload),
        )

        base_resp = ep_sdk_4pd_models.BaseResponse(
            code=response.json().get('code', None),
            data=response.json().get('data', None),
            message=response.json().get('message', None),
        )
        return ep_sdk_4pd_models.PredictDataResponse(response=base_resp)
