# _*_coding:utf-8 _*_
# Author: df_coding
# Time: 2025/4/18 上午9:27

import os
import sys
from pathlib import Path
from celery import current_app
from importlib.util import spec_from_file_location, module_from_spec


def locate_celery_config():
    """

    """
    # 检查环境变量
    env_path = os.getenv('CELERY_WORKER_PATH')
    if env_path:
        return Path(env_path).resolve().name + ".settings"

    # 项目根目录下的文件
    project_root = os.getenv('PYTHONPATH', '.').split(';')[-1]
    project_root = Path(project_root).resolve()
    project_config_path = project_root / 'settings.py'
    if project_config_path.exists():
        return "settings"

    # 返回包内默认路径
    return Path(__file__).parent.name + ".settings"


def load_tasks_dynamically(modules):
    """
        动态加载多个任务模块

    :param modules:
    :return:
    """
    for module_path in modules:
        if not os.path.exists(module_path):
            continue
        module_name = os.path.basename(module_path)[:-3]
        module = load_module_from_path(module_name, module_path)
        for attr in dir(module):
            obj = getattr(module, attr)
            if not callable(obj):
                continue
            if not hasattr(obj, 'delay'):
                continue

            if not obj.name:
                continue

            # print("DynamicTask ->", obj.name)
            current_app.tasks.register(obj)
    # print("__    -    ... __   -        _")


def load_module_from_path(module_name, module_path):
    """
    动态加载任意路径的模块，避免递归调用
    :param module_name: 模块的名称
    :param module_path: 模块的文件路径
    :return: 加载的模块对象
    """
    # 检查模块是否已经加载
    if module_name in sys.modules:
        return sys.modules[module_name]

    # 创建一个新的模块对象
    spec = spec_from_file_location(module_name, module_path)
    if spec is None:
        raise ImportError(f"Cannot find module at {module_path}")

    # 创建模块对象
    module = module_from_spec(spec)

    # 暂时将模块添加到 sys.modules，但不要执行代码
    sys.modules[module_name] = module

    # 执行模块代码（避免递归调用）
    try:
        spec.loader.exec_module(module)
    except RecursionError:
        # 如果发生递归调用，移除模块并抛出异常
        del sys.modules[module_name]
        raise RuntimeError("Recursive module loading detected. Check the module code.")

    return module
