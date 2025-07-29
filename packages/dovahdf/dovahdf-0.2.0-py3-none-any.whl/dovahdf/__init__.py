import sys
import types
import os

# 创建一个完整的 df 包
df_package = types.ModuleType('df')
df_package.__path__ = [os.path.join(os.path.dirname(__file__), 'df')]
sys.modules['df'] = df_package

# 这次我们不预先导入所有模块
# 而是安装一个导入钩子来拦截所有对 df.* 的导入

class DFFinder:
    def __init__(self, base_path):
        self.base_path = base_path
    
    def find_spec(self, fullname, path, target=None):
        if fullname == 'df' or fullname.startswith('df.'):
            # 转换为 dovahdf.df
            dovahdf_name = 'dovahdf.' + fullname
            return sys.meta_path[-1].find_spec(dovahdf_name, path, target)
        return None

# 将我们的导入钩子添加到 sys.meta_path 的开头
sys.meta_path.insert(0, DFFinder(os.path.dirname(__file__)))

# 然后导入子包
from . import df

# 为了方便使用，直接从子包导入常用功能
from .df.enhance import enhance, init_df
from .df.train import run_df_train

# 导出版本号
__version__ = getattr(df, '__version__', '0.1.0')