# 开发人员： Xiaoqiang
# 微信公众号:  XiaoqiangClub
# 开发时间： 2025-05-20
# 文件名称： AutoChrome/__init__.py
# 项目描述： init 文件
# 开发工具： PyCharm
from .utils.constants import (VERSION, AUTHOR, DESCRIPTION, EMAIL, IS_WINDOWS, log)
from .auto_chrome import AutoChrome

__title__ = "AutoChrome"
__version__ = VERSION
__author__ = AUTHOR
__description__ = DESCRIPTION

__all__ = [
    "__title__", "__version__", "__author__", "__description__",
    "VERSION", "AUTHOR", "DESCRIPTION", "EMAIL",
    "IS_WINDOWS", "log",
    "AutoChrome"
]
