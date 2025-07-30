class BaseRequest:
    """
    Model for BaseRequest
    """

    def __init__(self):
        self.api = None
        self.method = None
        self.content_type = None
        self.payload = None


class BaseResponse:
    """
    Model for BaseResponse
    """

    def __init__(
            self, code: int = None, data: dict = None, message: str = None, **kwargs
    ):
        self.code = code
        self.data = data
        self.message = message


class HistoryDataRequest(BaseRequest):
    """
    Model for HistoryDataRequest

    获取具体系统时间往前x天的数据（最晚时间为系统时间 D-2）
    特别注意：get_history_data 或 get_predict_data 会get_system_date进行检测，不可获取system_date以后得数据，避免数据穿越现象
    """

    def __init__(self, scope: str = None, system_date: str = None, days: int = None):
        """
        Args:
            scope: "weather","plant","market"
            system_date: 系统时间
            days: 表示systemDate之前days的数据
        """

        self.scope = scope
        self.system_date = system_date
        self.days = days

        super().__init__()
        self.api = f'/ep/api/sdk/get_history_data'
        self.method = 'POST'
        self.content_type = 'application/json'


class HistoryDataResponse(BaseResponse):
    """
    Model for HistoryDataResponse
    """

    def __init__(self, response: BaseResponse = None, **kwargs):
        super().__init__(
            code=response.code if response else None,
            data=response.data if response else None,
            message=response.message if response else None,
            **kwargs,
        )

class PredictDataRequest(BaseRequest):
    """
    Model for PredictDataRequest

    获取当前系统时间的预测数据（按照抓取时间，最晚时间为当前系统时间的d-1
    """

    def __init__(self, scope: str = None, system_date: str = None):
        """
        Args:
            scope: "weather","market"
            system_date: 系统时间
        """

        self.scope = scope
        self.system_date = system_date

        super().__init__()
        self.api = f'/ep/api/sdk/get_predict_data'
        self.method = 'POST'
        self.content_type = 'application/json'


class PredictDataResponse(BaseResponse):
    """
    Model for PredictDataResponse
    """

    def __init__(self, response: BaseResponse = None, **kwargs):
        super().__init__(
            code=response.code if response else None,
            data=response.data if response else None,
            message=response.message if response else None,
            **kwargs,
        )

class ModelOutputDirRequest(BaseRequest):
    """
    Model for ModelOutputDirRequest

    输出各策略的存放位置
    输入：
    线上环境：
    ${user.home}/strategyId/

    本地测试：
    ${user.home}/test/
    """

    def __init__(self, strategy_id: int = None):
        """
        Args:
            strategy_id: 是否线上环境
        """
        self.strategy_id = strategy_id

        super().__init__()
        self.api = f'/ep/api/sdk/model_output_dir'
        self.method = 'POST'
        self.content_type = 'application/json'


class ModelOutputDirResponse(BaseResponse):
    """
    Model for ModelOutputDirResponse
    """

    def __init__(self, response: BaseResponse = None, **kwargs):
        super().__init__(
            code=response.code if response else None,
            data=response.data if response else None,
            message=response.message if response else None,
            **kwargs,
        )

class RunStrategyRequest(BaseRequest):
    """
    Model for RunStrategyRequest

    获取此刻运行的策略模型基础信息
    """

    def __init__(self, strategy_id: int = None):
        """
        Args:
            strategy_id: 策略 id
        """
        self.strategy_id = strategy_id

        super().__init__()
        self.api = f'/ep/api/sdk/get_run_strategy'
        self.method = 'POST'
        self.content_type = 'application/json'


class RunStrategyResponse(BaseResponse):
    """
    Model for RunStrategyResponse
    """

    def __init__(self, response: BaseResponse = None, **kwargs):
        super().__init__(
            code=response.code if response else None,
            data=response.data if response else None,
            message=response.message if response else None,
            **kwargs,
        )

class CallTrainDoneRequest(BaseRequest):
    """
    Model for CallTrainDoneRequest

    回调设置模型策略训练完成，考虑是框架层调用 还是 用户自由设定
    输入：无，默认为EpSystem.get_run_strategy()["id"]
    """

    def __init__(
            self,
            strategy_id: int = None,
            script_strategy_id: int = None
    ):
        """
        Args:
            strategy_id
            script_strategy_id
        """
        self.strategy_id = strategy_id
        self.script_strategy_id = script_strategy_id

        super().__init__()
        self.api = f'/ep/api/sdk/call_train_done'
        self.method = 'POST'
        self.content_type = 'application/json'


class CallTrainDoneResponse(BaseResponse):
    """
    Model for CallTrainDoneResponse
    """

    def __init__(self, response: BaseResponse = None, **kwargs):
        super().__init__(
            code=response.code if response else None,
            data=response.data if response else None,
            message=response.message if response else None,
            **kwargs,
        )

class RsaKeyRequest(BaseRequest):
    """
    Model for RsaKeyRequest
    """

    def __init__(
            self
    ):

        super().__init__()
        self.api = f'/ep/api/sdk/get_rsa_key'
        self.method = 'GET'
        self.content_type = 'application/json'


class RsaKeyResponse(BaseResponse):
    """
    Model for RsaKeyResponse
    """

    def __init__(self, response: BaseResponse = None, **kwargs):
        super().__init__(
            code=response.code if response else None,
            data=response.data if response else None,
            message=response.message if response else None,
            **kwargs,
        )