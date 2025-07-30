import os
import importlib

__all__ = []

# 获取当前包的路径
package_dir = os.path.dirname(__file__)

# 遍历包目录下的所有文件
if package_dir:  # 确保 __file__ 可用且非空
    for module in os.listdir(package_dir):
        if module.endswith(".py") and module != "__init__.py":
            module_name = module[:-3]  # 去掉 ".py"
            # 动态导入模块
            mod = importlib.import_module(f".{module_name}", package=__name__)
            # 将模块中的所有公共名称（不以下划线开头）添加到包命名空间
            for name in dir(mod):
                if not name.startswith("_") and name not in globals():
                    globals()[name] = getattr(mod, name)
                    __all__.append(name)