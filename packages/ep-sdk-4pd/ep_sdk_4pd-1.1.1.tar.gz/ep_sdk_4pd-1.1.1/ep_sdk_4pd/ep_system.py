import json
import logging
import os
import rsa
import base64
import requests

from ep_sdk_4pd import models as ep_sdk_4pd_models
from datetime import datetime

from ep_sdk_4pd.models import ModelOutputDirRequest, RunStrategyRequest, CallTrainDoneRequest, RsaKeyRequest

# test 地址
# endpoint = 'http://172.27.88.56:6001'

# prod 地址
# endpoint = 'http://172.27.88.56:6601'

# 外网 地址
endpoint = 'http://82.157.231.254:6001'

Authorization = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJlbGVjdHJpY2l0eS1wbGF0Zm9ybSIsInN1YiI6IjEyMyIsImlhdCI6MTc0NjYwNjQ4NSwianRpIjoiMTIzXzE3NDY1Nzc2ODUxNDYiLCJ0eXBlIjoiYWNjZXNzIn0.Clrz_8j3aJlXTWPX-4DS0NxXN9idTcUIc0AtXOMIjd8'

def rsa_decrypt(privkey, ciphertext):
    decrypted = rsa.decrypt(base64.b64decode(ciphertext), privkey)
    return decrypted.decode('utf-8')

class EpSystem:

    @staticmethod
    def model_output_dir(is_online: bool = True):
        if is_online:
            # 从环境变量中获取策略id
            strategy_id = os.getenv('STRATEGY_ID')
            logging.info(f'strategy_id: {strategy_id}')

            if strategy_id is None:
                raise Exception('STRATEGY_ID is not set')
        else:
            # 线下环境，给固定的策略id
            strategy_id = 63
        request = ModelOutputDirRequest(strategy_id=strategy_id)
        full_url = f'{endpoint}{request.api}'
        headers = {
            'content-type': request.content_type,
            'Authorization': Authorization
        }

        payload = {
            'strategy_id': request.strategy_id
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
        response = ep_sdk_4pd_models.ModelOutputDirResponse(response=base_resp)

        if response.code == 200:
            return response.data
        else:
            return None

    @staticmethod
    def get_system_date(is_online: bool = True):
        """
        脚本每次预测的目标日，主要是拦截用户获取越界数据,用户不可修改
        """
        if is_online:
            # 线上环境,随着真实调用运行时间变化
            system_date = datetime.now().strftime('%Y-%m-%d')

            target_date = os.environ.get('TARGET_DATE')
            # target_date = 'JgAgrcfaQBI0h5YtLGGCjH92snKB3pUBOQs8yy0/mxMBdur0jNvAz6LzpU+Vq3QXsf36jy79WCrgVFo+0RwfUN338VJ9Qe+HwPfe0eq29De6eLD3nOl8xORj339dtSEdXq4dwc2mTaIxQc+erpv4acgQ7YVSDX6AuprwfW7c7qxthziqCqHxVm/qZwUkMsQ1fgzVLeICdscbCJbCD5GFYSpohaP5hRebutoa5FqyhYURA/4kxus98lJsENhnOZAACFdnCWDklpkKZyyOq0aKMd8Vv9SWX1LAZVTRjQ1GGuUPyOYjvnhUyNeRo3D85ODGBFeEju8rjDEB8LFSvX5d3Q=='
            if target_date is not None:
                rsa_data = EpSystem.get_rsa_key()
                if rsa_data:
                    rsa_private_key = rsa_data['rsa_private_key']
                    loaded_privkey = rsa.PrivateKey.load_pkcs1(rsa_private_key.encode('utf-8'))
                    decrypted_data = rsa_decrypt(loaded_privkey, target_date)
                    system_date = decrypted_data
        else:
            # 线下环境
            system_date = "2024-12-31"

        return system_date

    @staticmethod
    def get_run_strategy(is_online: bool = True):
        """
        获取此刻运行的策略模型基础信息
        :param is_online:
        :return:
        """
        if is_online:
            # 从环境变量中获取策略id
            strategy_id = os.getenv('STRATEGY_ID')
            logging.info(f'strategy_id: {strategy_id}')

            if strategy_id is None:
                raise Exception('STRATEGY_ID is not set')
        else:
            # 线下环境，给固定的策略id
            strategy_id = 1

        request = RunStrategyRequest(strategy_id=strategy_id)
        full_url = f'{endpoint}{request.api}'
        headers = {
            'content-type': request.content_type,
            'Authorization': Authorization
        }

        payload = {
            'strategy_id': request.strategy_id
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
        response = ep_sdk_4pd_models.RunStrategyResponse(response=base_resp)

        if response.code == 200:
            return response.data
        else:
            return None

    @staticmethod
    def call_train_done(
            strategy_id: int = None,
            script_strategy_id: int = None
    ):
        if (strategy_id is None
                or script_strategy_id is None
        ):
            strategy_id = os.getenv('STRATEGY_ID')
            script_strategy_id = os.getenv('SCRIPT_STRATEGY_ID')

        request = CallTrainDoneRequest(strategy_id=strategy_id,
                                       script_strategy_id=script_strategy_id)
        full_url = f'{endpoint}{request.api}'
        headers = {
            'content-type': request.content_type,
            'Authorization': Authorization
        }

        payload = {
            'strategy_id': request.strategy_id,
            'script_strategy_id': request.script_strategy_id
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
        response = ep_sdk_4pd_models.CallTrainDoneResponse(response=base_resp)

        if response.code == 200:
            return True
        else:
            return False

    @staticmethod
    def get_rsa_key():
        request = RsaKeyRequest()
        response = EpSystem.rsa_key(request=request)

        if response.code == 200:
            return response.data
        else:
            return None

    @staticmethod
    def rsa_key(
            request: ep_sdk_4pd_models.RsaKeyRequest = None,
    ) -> ep_sdk_4pd_models.RsaKeyResponse:

        full_url = f'{endpoint}{request.api}'
        headers = {
            'content-type': request.content_type,
            'Authorization': Authorization
        }

        response = requests.request(
            method=request.method,
            url=full_url,
            headers=headers,
        )

        base_resp = ep_sdk_4pd_models.BaseResponse(
            code=response.json().get('code', None),
            data=response.json().get('data', None),
            message=response.json().get('message', None),
        )
        return ep_sdk_4pd_models.RsaKeyResponse(response=base_resp)