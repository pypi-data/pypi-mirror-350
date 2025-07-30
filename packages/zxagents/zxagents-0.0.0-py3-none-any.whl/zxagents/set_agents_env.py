import os
import logging
from openai import AsyncOpenAI
from agents import (
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
)
import mlflow
from model_provider import ModelProvider
from typing import Optional

# 创建 .logs 目录（如果不存在）
logs_dir = '.logs'
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# 配置日志记录到文件
log_file = os.path.join(logs_dir, 'app.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)


def set_env(provider: Optional[ModelProvider] = None):
    """
    设置 OpenAI 客户端环境。

    :param provider: 模型提供程序，默认为 None
    """
    if provider is None:
        from model_provider import qwen
        provider = qwen

    # 获取配置值
    base_url = provider.get_config_value("base_url")
    api_key = provider.get_config_value("api_key")

    # 检查配置值是否为 None
    if base_url is None or api_key is None:
        error_msg = f"Missing base_url or api_key for provider {provider}"
        logging.error(error_msg)
        raise ValueError(error_msg)

    try:
        client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        set_default_openai_client(client=client, use_for_tracing=False)
        set_default_openai_api("chat_completions")
        set_tracing_disabled(disabled=True)
        logging.info("OpenAI client environment set successfully.")
    except Exception as e:
        logging.error(f"Error initializing AsyncOpenAI client: {e}")
        raise


def set_mlflow(experiment_name: str = "test", tracking_uri: str = "http://ai.zxtech.info:5000"):
    """
    设置 MLflow 环境。

    :param experiment_name: 实验名称，默认为 "test"
    :param tracking_uri: 跟踪 URI，默认为 "http://ai.zxtech.info:5000"
    """
    try:
        # 设置 MLflow 环境变量
        mlflow.set_tracking_uri(uri=tracking_uri)
        mlflow.set_experiment(experiment_name)
        # Enable MLflow automatic tracing for OpenAI with one line of code!
        mlflow.openai.autolog()
        logging.info("MLflow environment set successfully.")
    except Exception as e:
        logging.error(f"MLflow environment setting failed: {e}")


if __name__ == "__main__":
    set_env()
    #set_mlflow()

    # 传入自定义值
    #set_mlflow(experiment_name="new_experiment", tracking_uri="http://ai.zxtech.info:5000")