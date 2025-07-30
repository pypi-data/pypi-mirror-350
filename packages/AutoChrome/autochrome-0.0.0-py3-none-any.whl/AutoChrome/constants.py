"""
Author: xiaoqiang
Date: 2025-05-21 08:30:44
LastEditTime: 2025-05-23 12:05:36
LastEditors: xiaoqiang
Description: 常量定义文件
FilePath: \AutoChrome\AutoChrome\constants.py
"""

import os
import platform
from .logger import LoggerBase

# 版本号
VERSION = "0.0.1"
# 作者
AUTHOR = "Xiaoqiang"
# 邮箱
EMAIL = "xiaoqiangclub@hotmail.com"
# 项目描述
DESCRIPTION = "基于 DrissionPage 和 PyAutoGUI 制作的自用API封装库，便于实现网页自动化。"

# 当前运行的系统是否为Windows
IS_WINDOWS = platform.system() == "Windows"

# 项目根目录
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logger = LoggerBase(
    "AutoChrome", console_log_level="DEBUG", file_log_level="WARNING", log_file=None
)
log = logger.logger
