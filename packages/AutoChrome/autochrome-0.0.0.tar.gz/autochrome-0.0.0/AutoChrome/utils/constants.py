# 开发人员： Xiaoqiang
# 微信公众号:  XiaoqiangClub
# 开发时间： 2025-05-20
# 文件名称： AutoChrome/utils/constants.py
# 项目描述： 常量定义文件
# 开发工具： PyCharm
import os
import platform
from .logger import LoggerBase

# 版本号
VERSION = '0.0.1'
# 作者
AUTHOR = 'Xiaoqiang'
# 邮箱
EMAIL = 'xiaoqiangclub@hotmail.com'
# 项目描述
DESCRIPTION = '基于 DrissionPage 和 PyAutoGUI 制作的自用API封装库，便于实现网页自动化。'

# 当前运行的系统是否为Windows
IS_WINDOWS = platform.system() == 'Windows'

# 项目根目录
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logger = LoggerBase('AutoChrome', console_log_level='DEBUG', file_log_level='WARNING', log_file=None)
log = logger.logger
