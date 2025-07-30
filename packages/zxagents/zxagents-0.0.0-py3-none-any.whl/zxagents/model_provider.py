import os

class ModelProvider:
    def __init__(self, name, full_name, base_url, api_key):
        self.name = name
        self.full_name = full_name
        self.base_url = base_url
        self.api_key = os.getenv(api_key)

    def get_config_value(self, key):
        """
        获取指定配置值
        :param key: 配置键，如 'base_url' 或 'api_key'
        :return: 配置值，如果配置键不存在则返回 None
        """
        return getattr(self, key, None)


# 通义模型
qwen = ModelProvider(
    name="qwen",
    full_name="通义千问模型",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="QWEN_API_KEY",
)


# 火山引擎
ark = ModelProvider(
    name="ark",
    full_name="火山引擎模型",
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="ARK_API_KEY",
)

