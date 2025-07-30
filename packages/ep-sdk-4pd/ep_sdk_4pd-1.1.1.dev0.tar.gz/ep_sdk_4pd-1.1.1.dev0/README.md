# SDK 帮助文档

本说明文档旨在指导策略开发者如何使用平台提供的远程 SDK 仓库 `ep-sdk-4pd`，完成特征数据获取、模型开发与调试流程。

> ⚠️ ep-sdk-4pd SDK是平台为策略开发者提供的本地数据访问工具，用于访问结构化的示例数据，模拟真实环境中的策略开发流程。SDK 会自动识别运行环境，在本地开发时返回脱敏示例数据，结构与线上一致；在正式部署时连接真实数据库。

## 一、SDK 安装方式

SDK 已托管于远程私有仓库，用户可通过以下命令在本地完成安装：

```bash
pip install ep-sdk-4pd
```

安装成功后，策略脚本中可直接引入 SDK 提供的功能模块。

## 二、模块导入方式

平台策略执行环境中已预置 SDK 包 `ep-sdk-4pd`，用户在本地开发时可通过如下方式导入核心方法：

```python
from ep_sdk_4pd.ep_system import EpSystem
from ep_sdk_4pd.ep_data import EpData
```

## 三、系统环境接口（EpSystem）

系统接口统一封装于 `EpSystem` 类中，主要用于策略运行环境感知和训练/预测流程控制。

### 3.1 模型输出路径：`EpSystem.model_output_dir()`

- **定义**：获取模型输出目录路径

- **线上环境返回**：`/home/{user}/strategyId/`

- **本地调试返回**：`/home/{user}/test/`

### 3.2 获取系统时间：`EpSystem.get_system_date()`

- **定义**：获取平台运行时系统时间，作为训练或预测数据的参考时间基准。用户不可自定义修改。

- **本地调试返回**：固定测试值，如 `"2024-12-31"`

- **线上运行返回**：随运行时间变化，如 `"2025-04-01"`

### 3.3 获取运行策略信息：`EpSystem.get_run_strategy()`

- **定义**：获取当前正在运行的策略上下文信息

- **返回示例（测试环境）**：

```python
{
  "id": 1,
  "name": "空仓策略",
  "description": "不参考任何信息，96节点全部报0",
  "plant": "test站点",
  "countyCode": 1000100
}
```

### 3.4 训练完成通知：`EpSystem.call_train_done()`

- **定义**：用于回调通知平台当前策略训练已完成。

- **默认行为**：调用时会自动读取当前运行策略 ID，用户无需传参。

- **返回值**：`True`（成功）或 `False`（失败）



## 四、特征数据接口（EpData）

数据接口封装于 `EpData` 类中，用于获取结构化输入数据，包括天气、市场、电厂等特征。数据按系统时间校验，不可穿越未来。

### 4.1 数据获取规则

- 可获取数据时间段为：`2024-01-01 ~ 2024-12-31`

- 推理模拟从 `2025-01-01` 开始顺序执行

### 4.2 获取历史数据：`EpData.get_history_data(scope: str, days: int)`

- **定义**：获取当前系统时间向前指定天数的数据（最晚支持到 D-2）

- **参数说明：**

  - `scope`：选择数据模块，支持 `["weather", "plant", "market"]`

  - `days`：获取当前系统时间前 N 天的数据

- **示例调用：**

```python
from ep_sdk_4pd.ep_data import EpData

# 获取全量的历史特征
data = EpData.get_history_data(days=7)
# 获取天气的历史特征
weather_data = EpData.get_history_data(scope="weather", days=7)
```

- **返回格式：**

```python
data = {
    "weather": pd.DataFrame(...),
    "plant": pd.DataFrame(...),
    "market": pd.DataFrame(...)
}
weather_data = {
    "weather": pd.DataFrame(...)
}
```

- **字段详解：**

  - `market`：聚合电力交易市场相关信息，如价格、电量、调度负荷、联络线、新能源出力等

  - `plant`：聚合特定发电场站相关运行指标，站点电价、电量等

  - `weather`：聚合天气相关数据，如天气实况、未来预报、气象背景等

- 更多字段说明，请参考平台对应的「数据字典文档」。

### 4.3 获取预测数据：`EpData.get_predict_data(scope: str)`

- **定义**：获取当前系统时间的预测数据（最晚为 D-1）

- **参数说明：**

  - `scope`：可选数据范围，与 `get_history_data` 相同

- **示例调用：**

```python
from ep_sdk_4pd.ep_data import EpData

# 获取市场和天气的预测特征
data = EpData.get_predict_data(scope="market,weather")
```

- **返回格式：**

```python
data = {
    "weather": pd.DataFrame(...),
    "market": pd.DataFrame(...)
}
```

## 五、环境适配说明

- 本地调试环境下，SDK 返回脱敏示例数据，用于验证模型逻辑与调试开发流程。

- 部署上线后，SDK 自动连接真实数据库，返回真实交易场景中的数据。

- 开发者无需修改代码逻辑，环境判断与数据源切换由 SDK 内部自动处理。

## 六、常见问题 FAQ

### Q1：如何确定当前系统时间？

可通过 `EpSystem.get_system_date()` 获取，格式为 `YYYY-MM-DD`。

### Q2：为什么我的数据不包含最新日期？

`get_history_data` 返回最晚到系统时间的 D-2 日数据，`get_predict_data` 返回系统时间的 D-1 日预测数据。

### Q3：模型训练完成后如何保存模型？

平台会在运行策略时创建独立的模型输出目录（通过 `EpSystem.model_output_dir()` 获取），用于保存用户的模型对象或其他中间结果。

建议使用常见的 Python 序列化方案保存模型，如：

**方式一：pickle 序列化（推荐用于简单对象）**

```Python
import pickle
from ep_sdk_4pd.ep_system import EpSystem

out_dict = {"price_model": model1, "power_model": model2}
with open(f"{EpSystem.model_output_dir()}/model.pickle", "wb") as f:
    pickle.dump(out_dict, f)
```

**方式二：joblib 序列化（推荐用于大型模型）**

```Python
from joblib import dump
from ep_sdk_4pd.ep_system import EpSystem

model_path = f"{EpSystem.model_output_dir()}/model.joblib"
dump(your_model, model_path)
```

**方式三：自定义格式存储（如 JSON/CSV/HDF5 等）** 对于不适合直接 pickle 的模型（如深度学习框架模型、含依赖项对象），也可通过保存权重、参数配置等方式进行落盘。

### Q4：如何判断当前策略运行上下文？

通过 `EpSystem.get_run_strategy()` 可获取策略 ID、配置等元信息，便于调试和日志输出。

如需获取最新数据字段说明、SDK 更新日志或接口文档，请前往平台「数据文档中心」或联系管理员。