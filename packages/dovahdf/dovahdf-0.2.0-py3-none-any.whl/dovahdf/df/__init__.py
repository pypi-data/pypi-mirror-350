from .config import config
from .enhance import enhance, init_df
from .version import version
from .train import run_df_train  # 添加 run_df_train 函数

# 预加载配置文件
try:
    import os
    # 首先检查环境变量
    if "DF_CONFIG_PATH" in os.environ and os.path.isfile(os.environ["DF_CONFIG_PATH"]):
        config.load(os.environ["DF_CONFIG_PATH"], allow_defaults=True)
    else:
        # 然后尝试Docker环境和其他常见位置
        possible_paths = [
            "/workspace/AudioClarity/models/DeepFilterNet2/config.ini",
            os.path.join(os.getcwd(), "models/DeepFilterNet2/config.ini"),
            os.path.join(os.getcwd(), "config.ini"),
            "/AudioClarity/models/DeepFilterNet2/config.ini"
        ]
        for p in possible_paths:
            if os.path.isfile(p):
                config.load(p, allow_defaults=True)
                break
except Exception as e:
    # 静默失败，不打印错误消息，以避免干扰正常导入
    pass

# 更新 __all__ 列表，包含 run_df_train
__all__ = ["config", "version", "enhance", "init_df", "run_df_train"]
__version__ = version