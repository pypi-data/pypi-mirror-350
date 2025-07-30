"""
Author: xiaoqiang
Date: 2025-05-21 08:30:44
LastEditTime: 2025-05-25 21:31:13
Description: 自动化页面
FilePath: /AutoChrome/AutoChrome/auto_chrome.py
"""

from typing import List, Tuple, Union, Optional, Literal
from http.cookiejar import Cookie, CookieJar
from AutoChrome.utils.constants import logger, log, IS_WINDOWS

# 导入说明：https://drissionpage.cn/get_start/import
from DrissionPage.items import ChromiumTab
from DrissionPage import Chromium, ChromiumOptions, SessionOptions


class AutoChrome:
    def __init__(
        self,
        start_url: Optional[str] = None,
        dp_chrome: Optional[Chromium] = None,
        chrome_options: Union[str, int, ChromiumOptions, None] = None,
        session_options: Union[SessionOptions, None, bool] = None,
        headless: bool = False,
        auto_port: bool = False,
        user_data_path: Optional[str] = None,
        auto_close: bool = False,
        show_log_level: str = "WARNING",
    ):
        """
        网页自动化
        多浏览器操作文档：
        https://drissionpage.cn/browser_control/connect_browser/#%EF%B8%8F-%E5%A4%9A%E6%B5%8F%E8%A7%88%E5%99%A8%E5%85%B1%E5%AD%98

        :param start_url: 启动页面
        :param dp_chrome: DrissionPage 的 Chromium 对象：https://drissionpage.cn/browser_control/connect_browser#%EF%B8%8F-chromium%E5%88%9D%E5%A7%8B%E5%8C%96%E5%8F%82%E6%95%B0
        :param chrome_options: Chromium 的 addr_or_opts 参数，注意：仅当 dp_chrome=None 时有效！
        :param session_options: Chromium 的 session_options 参数，注意：仅当 dp_chrome=None 时有效！
        :param headless: 是否启用无头模式
        :param auto_port: 是否自动分配端口，仅当 chrome_options=None 时生效：https://drissionpage.cn/browser_control/connect_browser#-auto_port%E6%96%B9%E6%B3%95
        :param user_data_path: 设置用户数据路径：https://drissionpage.cn/browser_control/connect_browser#-%E5%8D%95%E7%8B%AC%E6%8C%87%E5%AE%9A%E6%9F%90%E4%B8%AA%E7%94%A8%E6%88%B7%E6%96%87%E4%BB%B6%E5%A4%B9
        :param auto_close: 是否自动关闭浏览器
        :param show_log_level: 显示的日志等级，可选值：DEBUG, INFO, WARNING, ERROR, CRITICAL
        """
        # 设置日志显示的等级
        logger.set_log_level(show_log_level)

        # 启动页面
        self.start_url = start_url
        self.auto_close = auto_close

        # 浏览器参数
        chrome_options = chrome_options or ChromiumOptions()
        chrome_options.headless(headless)  # 启用无头模式
        chrome_options = chrome_options.auto_port(auto_port)  # 自动分配端口
        if user_data_path:  # 设置用户数据路径
            chrome_options = chrome_options.set_user_data_path(user_data_path)

        # 创建浏览器对象
        self.browser = dp_chrome or Chromium(
            addr_or_opts=chrome_options, session_options=session_options
        )
        self.latest_tab = self.browser.latest_tab

        #  启动页面
        if self.start_url:
            self.latest_tab.get(self.start_url)

    def get_cookies(
        self,
        tab: Optional[Chromium] = None,
        all_info: bool = False,
        return_type: Literal["list", "str", "dict", "json"] = "list",
    ) -> Union[List[dict], str, dict]:
        """
        获取 标签页的cookies
        https://drissionpage.cn/SessionPage/get_page_info/#%EF%B8%8F%EF%B8%8F-cookies-%E4%BF%A1%E6%81%AF

        :param tab: 标签页，默认为: None, 使用 self.latest_tab
        :param all_info: 是否获取所有信息，默认为: False, 仅获取 name、value、domain 的值
        :param return_type: 返回类型，默认为: list, 可选值：list、str、dict、json, 注意：str 和 dict 都只会保留 'name'和 'value'字段; json 返回的是 json格式的字符串
        :return:
        """
        tab = tab or self.latest_tab
        c = tab.cookies(all_info=all_info)
        if return_type == "list":
            return c
        elif return_type == "str":
            return c.as_str()
        elif return_type == "dict":
            return c.as_dict()
        elif return_type == "json":
            return c.as_json()
        else:
            raise ValueError("return_type 参数错误！")

    def set_cookies(
        self,
        cookies: Union[Cookie, str, dict, list, tuple, CookieJar],
        tab: Optional[Chromium] = None,
        refresh: bool = True,
        verify_str: Optional[str] = None,
    ) -> Optional[bool]:
        """
        给标签页设置 cookies
        https://drissionpage.cn/tutorials/functions/set_cookies

        :param cookies: cookies 的值，支持字符串和字典格式
        :param tab: 标签页，默认为: None, 使用 self.latest_tab
        :param refresh: 是否刷新页面，默认为: True, 刷新页面
        :param verify: 是否验证 cookies 设置成功，默认为: None, 不验证; 为 字符串 时会自动刷新页面。并且验证页面是否包含 verify_str 字符串.
        :return: 如果 verify=True，则返回一个布尔值，表示 cookies 是否设置成功；否则返回 None
        """
        tab = tab or self.latest_tab
        tab.set.cookies(cookies)

        if refresh or verify_str:
            log.info("刷新页面...")
            tab.refresh()

        if verify_str:
            log.info("正在验证 cookies 是否设置成功...")
            if verify_str in tab.html:
                log.info("cookies 设置成功！")
                return True
            else:
                log.error("cookies 设置失败/已失效！")
                return False

    def hide_tab(self, tab: Optional[Chromium] = None) -> None:
        """
        此方法用于隐藏签页窗口，但是会导致整个浏览器窗口被隐藏。
        与 headless 模式不一样，这个方法是直接隐藏浏览器进程。在任务栏上也会消失。
        只支持 Windows 系统，并且必需已安装 pypiwin32 库才可使用。
        pip install -i https://mirrors.aliyun.com/pypi/simple/ -U pypiwin32
        https://drissionpage.cn/browser_control/page_operation/#-setwindowhide

        :param tab: 标签页对象，如果为 None，则使用 self.latest_tab
        :return:
        """
        if not IS_WINDOWS:
            log.error("此方法仅支持 Windows 系统！")
            return

        log.info("隐藏浏览器窗口...")
        tab = tab or self.latest_tab
        tab.set.window.hide()

    def show_tab(self, tab: Optional[Chromium] = None) -> None:
        """
        显示标签页，该操作会显示整个浏览器。
        :param tab: 标签页对象，如果为 None，则使用 self.latest_tab
        :return:
        """
        if not IS_WINDOWS:
            log.error("此方法仅支持 Windows 系统！")
            return

        log.info("显示浏览器窗口...")
        tab = tab or self.latest_tab
        tab.set.window.show()

    def close_browser(
        self,
        close_current_tab=False,
        close_other_tabs=False,
        close_session=False,
        timeout: float = 3,
        kill_process=False,
        del_user_data=False,
    ) -> List[bool]:
        """
        关闭浏览器
        :param close_current_tab: 关闭当前标签页
        :param close_other_tabs: 关闭其他标签页，仅当 close_current_tab=True 时生效
        :param close_session: 是否同时关闭内置 Session 对象，只对自己有效，仅当 close_current_tab=True 时生效
        :param timeout: 关闭浏览器超时时间，单位秒
        :param kill_process: 是否立刻强制终止进程
        :param del_user_data: 是否删除用户数据
        :return:
        """
        try:
            if close_current_tab:  # 关闭当前标签页
                log.info("正在关闭标签页，请稍等...")
                self.latest_tab.close(others=close_other_tabs, session=close_session)
            close_tab = True
        except Exception as e:
            log.error(f"关闭标签页出错: {e}")
            close_tab = False

        try:
            # 关闭浏览器
            log.info("正在关闭浏览器，请稍等...")
            self.browser.quit(
                timeout=timeout, force=kill_process, del_data=del_user_data
            )
            log.info("浏览器已关闭！")
            close_browser = True
        except Exception as e:
            log.error(f"关闭浏览器出错: {e}")
            close_browser = False

        return [close_tab, close_browser]

    def __del__(self) -> None:
        """
        关闭浏览器
        """
        if not self.auto_close:
            return

        self.close_browser()

    def ele_for_data(
        self,
        selector: Union[str, Tuple[str]],
        tab: Optional[ChromiumTab] = None,
        index: int = 1,
        timeout: Optional[float] = None,
    ):
        """
        获取单个静态元素用于提取数据
        https://drissionpage.cn/browser_control/get_elements/find_in_object/#-s_ele

        :param selector: 元素的定位信息。可以是查询字符串，或 loc 元组：https://drissionpage.cn/browser_control/get_elements/syntax#%EF%B8%8F%EF%B8%8F-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5
        :param tab: 标签页对象，如果为 None，则使用 self.latest_tab
        :param index: 获取第几个匹配的元素，从 1 开始，可输入负数表示从后面开始数，默认为 1
        :param timeout: 等待元素出现的超时时间（秒），默认为: None 使用页面对象设置
        :return: 元素对象
        """
        tab = tab or self.latest_tab

        return tab.s_ele(selector, index=index, timeout=timeout)

    def eles_for_data(
        self,
        selector: Union[str, Tuple[str]],
        tab: Optional[ChromiumTab] = None,
        timeout: Optional[float] = None,
    ):
        """
        获取静态元素用于提取数据
        https://drissionpage.cn/browser_control/get_elements/find_in_object/#-s_eles

        :param selector: 元素的定位信息。可以是查询字符串，或 loc 元组
        :param tab: 标签页对象，如果为 None，则使用 self.latest_tab
        :param timeout: 等待元素出现的超时时间（秒），默认为: None 使用页面对象设置
        :return: 元素对象
        """
        tab = tab or self.latest_tab

        return tab.s_eles(selector, timeout=timeout)

    def xpath_for_data(
        self,
        xpath: str,
        tab: Optional[ChromiumTab] = None,
        index: Optional[int] = 1,
        timeout: Optional[float] = None,
    ):
        """
        使用 Xpath 获取单个静态元素用于提取数据
        https://drissionpage.cn/browser_control/get_elements/syntax/#-xpath-%E5%8C%B9%E9%85%8D%E7%AC%A6-xpath

        :param xpath: Xpath表达式，可 F12 下直接鼠标右键——复制XPath: 用 xpath 在元素下查找时，最前面 // 或 / 前面的 . 可以省略。
        :param tab: 标签页对象，如果为 None，则使用 self.latest_tab
        :param index: 获取第几个匹配的元素，从 1 开始，可输入负数表示从后面开始数，默认为 1。当 index=None 时，返回所有匹配的元素，相当于 s_eles。
        :param timeout: 等待元素出现的超时时间（秒），默认为: None 使用页面对象设置
        :return: 元素对象
        """
        tab = tab or self.latest_tab
        if index is None:
            return tab.s_eles(f"xpath:{xpath}", timeout=timeout)

        return tab.s_ele(f"xpath:{xpath}", index=index, timeout=timeout)

    def xpath_for_action(
        self,
        xpath: str,
        tab: Optional[ChromiumTab] = None,
        index: Optional[int] = 1,
        timeout: Optional[float] = None,
    ):
        """
        使用 Xpath 定位单个元素用于执行操作
        https://drissionpage.cn/browser_control/get_elements/find_in_object/#-ele

        :param xpath: 元素的定位信息。可以是查询字符串，或 loc 元组：https://drissionpage.cn/browser_control/get_elements/syntax#%EF%B8%8F%EF%B8%8F-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5
        :param tab: 标签页对象，如果为 None，则使用 self.latest_tab
        :param index: 获取第几个匹配的元素，从 1 开始，可输入负数表示从后面开始数，默认为 1
        :param timeout: 等待元素出现的超时时间（秒），默认为: None 使用页面对象设置
        :return: 元素对象
        """
        tab = tab or self.latest_tab

        return tab.ele(f"xpath:{xpath}", index=index, timeout=timeout)

    def ele_for_action(
        self,
        selector: Union[str, Tuple[str]],
        tab: Optional[ChromiumTab] = None,
        index: Optional[int] = 1,
        timeout: Optional[float] = None,
    ):
        """
        定位单个元素用于执行操作
        https://drissionpage.cn/browser_control/get_elements/find_in_object/#-ele

        :param selector: 元素的定位信息。可以是查询字符串，或 loc 元组：https://drissionpage.cn/browser_control/get_elements/syntax#%EF%B8%8F%EF%B8%8F-%E5%9F%BA%E6%9C%AC%E6%A6%82%E5%BF%B5
        :param tab: 标签页对象，如果为 None，则使用 self.latest_tab
        :param index: 获取第几个匹配的元素，从 1 开始，可输入负数表示从后面开始数，默认为 1
        :param timeout: 等待元素出现的超时时间（秒），默认为: None 使用页面对象设置
        :return: 元素对象
        """
        tab = tab or self.latest_tab

        return tab.ele(selector, index=index, timeout=timeout)
