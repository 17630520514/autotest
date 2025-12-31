import allure
from playwright.sync_api import Page, TimeoutError, Locator
from config.config import TIMEOUT
from utils.logger import Logger
from typing import Union, Tuple


class BasePage:
    """页面基类,封装通用的页面操作方法"""

    def __init__(self, page: Page):
        self.page = page
        self.timeout = TIMEOUT
        self.logger = Logger(self.__class__.__name__)

    def _get_locator(self, locator: Union[str, Tuple[str, str]]) -> Locator:
        """智能定位器：自动识别定位器类型并返回 Playwright Locator

        Args:
            locator: 定位器，支持三种格式：
                - 元组 ("role", "name"): 使用 get_by_role
                - 字符串 "#id" 或 ".class": 使用 CSS 选择器
                - 字符串 "//xpath": 使用 XPath

        Returns:
            Playwright Locator 对象

        Examples:
            # Role 定位器
            locator = self._get_locator(("button", "提交"))

            # CSS 定位器
            locator = self._get_locator("#submit-btn")

            # XPath 定位器
            locator = self._get_locator("//button[@id='submit']")
        """
        if isinstance(locator, tuple):
            # 元组形式：使用 get_by_role
            role, name = locator
            self.logger.debug(f"使用 Role 定位器: role={role}, name={name}")
            return self.page.get_by_role(role, name=name)
        elif isinstance(locator, str):
            # 字符串形式：判断是 XPath 还是 CSS
            if locator.startswith(("//", "(", "./")):
                # XPath 定位器
                self.logger.debug(f"使用 XPath 定位器: {locator}")
                return self.page.locator(f"xpath={locator}")
            else:
                # CSS 选择器
                self.logger.debug(f"使用 CSS 定位器: {locator}")
                return self.page.locator(locator)
        else:
            raise ValueError(f"不支持的定位器类型: {type(locator)}, 值: {locator}")

    def _get_locator_description(self, locator: Union[str, Tuple[str, str]]) -> str:
        """获取定位器的描述字符串（用于日志）

        Args:
            locator: 定位器

        Returns:
            定位器的描述字符串
        """
        if isinstance(locator, tuple):
            role, name = locator
            return f"Role({role}, '{name}')"
        else:
            return f"'{locator}'"

    @allure.step("导航到页面: {url}")
    def navigate(self, url: str):
        """导航到指定URL"""
        try:
            self.logger.info(f"导航到页面: {url}")
            self.page.goto(url)
            self.logger.info(f"成功加载页面: {url}")
        except Exception as e:
            self.logger.error(f"导航失败: {url}, 错误: {str(e)}")
            raise

    @allure.step("点击元素")
    def click(self, locator: Union[str, Tuple[str, str]]):
        """智能点击元素 - 支持 CSS/XPath 字符串或 Role 元组

        Args:
            locator: 定位器，支持：
                - CSS: "#id" 或 ".class"
                - XPath: "//button[@id='submit']"
                - Role: ("button", "提交")
        """
        try:
            loc_desc = self._get_locator_description(locator)
            self.logger.info(f"尝试点击元素: {loc_desc}")
            self._get_locator(locator).click(timeout=self.timeout)
            self.logger.info(f"成功点击元素: {loc_desc}")
        except TimeoutError:
            error_msg = f"元素未找到或不可点击: {loc_desc}"
            self.logger.error(error_msg)
            # 转换为 AssertionError，让 Allure 显示为 Failed (红色) 而非 Broken (黄色)
            raise AssertionError(error_msg)
        except Exception as e:
            self.logger.error(f"点击元素失败: {loc_desc}, 错误: {str(e)}")
            raise

    @allure.step("填充元素")
    def fill(self, locator: Union[str, Tuple[str, str]], text: str):
        """智能填充输入框 - 支持 CSS/XPath 字符串或 Role 元组

        Args:
            locator: 定位器，支持：
                - CSS: "#username" 或 ".input-field"
                - XPath: "//input[@name='username']"
                - Role: ("textbox", "用户名")
            text: 要填充的文本
        """
        try:
            loc_desc = self._get_locator_description(locator)
            self.logger.info(f"尝试填充元素: {loc_desc}, 内容: {text}")
            self._get_locator(locator).fill(text, timeout=self.timeout)
            self.logger.info(f"成功填充元素: {loc_desc}")
        except TimeoutError:
            error_msg = f"输入框未找到: {loc_desc}"
            self.logger.error(error_msg)
            # 转换为 AssertionError，让 Allure 显示为 Failed (红色)
            raise AssertionError(error_msg)
        except Exception as e:
            self.logger.error(f"填充元素失败: {loc_desc}, 错误: {str(e)}")
            raise

    @allure.step("获取元素文本")
    def get_text(self, locator: Union[str, Tuple[str, str]]) -> str:
        """智能获取元素文本 - 支持 CSS/XPath 字符串或 Role 元组

        Args:
            locator: 定位器，支持：
                - CSS: ".title" 或 "#heading"
                - XPath: "//h1[@class='title']"
                - Role: ("heading", "页面标题")

        Returns:
            元素的文本内容
        """
        try:
            loc_desc = self._get_locator_description(locator)
            self.logger.info(f"尝试获取元素文本: {loc_desc}")
            text = self._get_locator(locator).text_content(timeout=self.timeout)
            self.logger.info(f"成功获取文本: {loc_desc}, 内容: {text}")
            return text
        except TimeoutError:
            error_msg = f"元素未找到,无法获取文本: {loc_desc}"
            self.logger.error(error_msg)
            # 转换为 AssertionError，让 Allure 显示为 Failed (红色)
            raise AssertionError(error_msg)
        except Exception as e:
            self.logger.error(f"获取文本失败: {loc_desc}, 错误: {str(e)}")
            raise

    @allure.step("检查元素可见性")
    def is_visible(self, locator: Union[str, Tuple[str, str]]) -> bool:
        """智能检查元素是否可见 - 支持 CSS/XPath 字符串或 Role 元组

        Args:
            locator: 定位器，支持：
                - CSS: ".modal" 或 "#popup"
                - XPath: "//div[@class='modal']"
                - Role: ("dialog", "确认弹窗")

        Returns:
            True 表示可见，False 表示不可见
        """
        try:
            loc_desc = self._get_locator_description(locator)
            visible = self._get_locator(locator).is_visible()
            if visible:
                self.logger.info(f"元素可见: {loc_desc}")
            else:
                self.logger.warning(f"元素不可见: {loc_desc}")
            return visible
        except Exception as e:
            self.logger.error(f"检查元素可见性失败: {loc_desc}, 错误: {str(e)}")
            return False

    @allure.step("等待元素出现")
    def wait_for_selector(self, locator: Union[str, Tuple[str, str]]):
        """智能等待元素出现 - 支持 CSS/XPath 字符串或 Role 元组

        Args:
            locator: 定位器，支持：
                - CSS: ".loading" 或 "#spinner"
                - XPath: "//div[@class='loading']"
                - Role: ("status", "加载中")
        """
        try:
            loc_desc = self._get_locator_description(locator)
            self.logger.info(f"等待元素出现: {loc_desc}")
            self._get_locator(locator).wait_for(state="visible", timeout=self.timeout)
            self.logger.info(f"元素已出现: {loc_desc}")
        except TimeoutError:
            error_msg = f"等待超时,元素未出现: {loc_desc}"
            self.logger.error(error_msg)
            # 转换为 AssertionError，让 Allure 显示为 Failed (红色)
            raise AssertionError(error_msg)
        except Exception as e:
            self.logger.error(f"等待元素失败: {loc_desc}, 错误: {str(e)}")
            raise

    @allure.step("点击角色元素: {role} - {name}")
    def click_by_role(self, role: str, name: str):
        """通过角色和名称点击元素 (基于可访问性)"""
        try:
            self.logger.info(f"尝试点击 {role}: {name}")
            self.page.get_by_role(role, name=name).click(timeout=self.timeout)
            self.logger.info(f"成功点击 {role}: {name}")
        except TimeoutError:
            self.logger.error(f"元素未找到或不可点击: {role} - {name}")
            raise
        except Exception as e:
            self.logger.error(f"点击元素失败: {role} - {name}, 错误: {str(e)}")
            raise

    @allure.step("填充角色元素: {role} - {name}, 内容: {text}")
    def fill_by_role(self, role: str, name: str, text: str):
        """通过角色和名称填充输入框 (基于可访问性)"""
        try:
            self.logger.info(f"尝试填充 {role}: {name}, 内容: {text}")
            self.page.get_by_role(role, name=name).fill(text, timeout=self.timeout)
            self.logger.info(f"成功填充 {role}: {name}")
        except TimeoutError:
            self.logger.error(f"输入框未找到: {role} - {name}")
            raise
        except Exception as e:
            self.logger.error(f"填充元素失败: {role} - {name}, 错误: {str(e)}")
            raise

    @allure.step("获取角色元素文本: {role} - {name}")
    def get_text_by_role(self, role: str, name: str) -> str:
        """通过角色和名称获取元素文本 (基于可访问性)"""
        try:
            self.logger.info(f"尝试获取元素文本: {role} - {name}")
            text = self.page.get_by_role(role, name=name).text_content(timeout=self.timeout)
            self.logger.info(f"成功获取文本: {role} - {name}, 内容: {text}")
            return text
        except TimeoutError:
            self.logger.error(f"元素未找到,无法获取文本: {role} - {name}")
            raise
        except Exception as e:
            self.logger.error(f"获取文本失败: {role} - {name}, 错误: {str(e)}")
            raise
        
    
    @allure.step("检查元素是否选中")
    def is_checked(self, locator: Union[str, Tuple[str, str]]) -> bool:
        """智能检查元素是否选中 - 支持 CSS/XPath 字符串或 Role 元组

        Args:
            locator: 定位器，支持：
                - CSS: "#remember-me" 或 ".checkbox"
                - XPath: "//input[@type='checkbox']"
                - Role: ("checkbox", "记住我")

        Returns:
            True 表示选中，False 表示未选中
        """
        try:
            loc_desc = self._get_locator_description(locator)
            checked = self._get_locator(locator).is_checked()
            if checked:
                self.logger.info(f"元素已选中: {loc_desc}")
            else:
                self.logger.warning(f"元素未选中: {loc_desc}")
            return checked
        except Exception as e:
            self.logger.error(f"检查元素是否选中失败: {loc_desc}, 错误: {str(e)}")
            return False

    @allure.step("选中元素")
    def check(self, locator: Union[str, Tuple[str, str]]):
        """智能选中元素 - 支持 CSS/XPath 字符串或 Role 元组

        Args:
            locator: 定位器，支持：
                - CSS: "#remember" 或 ".agree-checkbox"
                - XPath: "//input[@name='remember']"
                - Role: ("checkbox", "记住我")
        """
        try:
            loc_desc = self._get_locator_description(locator)
            self.logger.info(f"尝试选中元素: {loc_desc}")
            self._get_locator(locator).check(timeout=self.timeout)
            self.logger.info(f"成功选中元素: {loc_desc}")
        except TimeoutError:
            error_msg = f"元素未找到: {loc_desc}"
            self.logger.error(error_msg)
            # 转换为 AssertionError，让 Allure 显示为 Failed (红色)
            raise AssertionError(error_msg)
        except Exception as e:
            self.logger.error(f"选中元素失败: {loc_desc}, 错误: {str(e)}")
            raise

    @allure.step("取消选中元素")
    def uncheck(self, locator: Union[str, Tuple[str, str]]):
        """智能取消选中元素 - 支持 CSS/XPath 字符串或 Role 元组

        Args:
            locator: 定位器，支持：
                - CSS: "#remember" 或 ".agree-checkbox"
                - XPath: "//input[@name='remember']"
                - Role: ("checkbox", "记住我")
        """
        try:
            loc_desc = self._get_locator_description(locator)
            self.logger.info(f"尝试取消选中元素: {loc_desc}")
            self._get_locator(locator).uncheck(timeout=self.timeout)
            self.logger.info(f"成功取消选中元素: {loc_desc}")
        except TimeoutError:
            error_msg = f"元素未找到: {loc_desc}"
            self.logger.error(error_msg)
            # 转换为 AssertionError，让 Allure 显示为 Failed (红色)
            raise AssertionError(error_msg)
        except Exception as e:
            self.logger.error(f"取消选中元素失败: {loc_desc}, 错误: {str(e)}")
            raise

    @allure.step("检查角色元素是否选中: {role} - {name}")
    def is_checked_by_role(self, role: str, name: str) -> bool:
        """检查角色元素是否选中（基于可访问性）

        Args:
            role: 元素角色，如 "checkbox", "radio"
            name: 可访问名称

        Returns:
            bool: True 表示选中，False 表示未选中

        Examples:
            # 检查复选框是否选中
            is_checked = self.is_checked_by_role("checkbox", "记住我")

            # 检查单选按钮是否选中
            is_selected = self.is_checked_by_role("radio", "男")
        """
        try:
            self.logger.info(f"尝试检查 {role}: {name} 是否选中")
            checked = self.page.get_by_role(role, name=name).is_checked(timeout=self.timeout)
            if checked:
                self.logger.info(f"元素已选中: {role} - {name}")
            else:
                self.logger.warning(f"元素未选中: {role} - {name}")
            return checked
        except TimeoutError:
            self.logger.error(f"元素未找到: {role} - {name}")
            raise
        except Exception as e:
            self.logger.error(f"检查元素是否选中失败: {role} - {name}, 错误: {str(e)}")
            return False

    @allure.step("选中角色元素: {role} - {name}")
    def check_by_role(self, role: str, name: str):
        """选中角色元素（复选框/单选按钮）

        Args:
            role: 元素角色，如 "checkbox", "radio"
            name: 可访问名称

        Examples:
            # 选中复选框
            self.check_by_role("checkbox", "记住我")
        """
        try:
            self.logger.info(f"尝试选中 {role}: {name}")
            self.page.get_by_role(role, name=name).check(timeout=self.timeout)
            self.logger.info(f"成功选中 {role}: {name}")
        except TimeoutError:
            self.logger.error(f"元素未找到: {role} - {name}")
            raise
        except Exception as e:
            self.logger.error(f"选中元素失败: {role} - {name}, 错误: {str(e)}")
            raise

    @allure.step("取消选中角色元素: {role} - {name}")
    def uncheck_by_role(self, role: str, name: str):
        """取消选中角色元素（复选框）

        Args:
            role: 元素角色，通常是 "checkbox"
            name: 可访问名称

        Examples:
            # 取消选中复选框
            self.uncheck_by_role("checkbox", "记住我")
        """
        try:
            self.logger.info(f"尝试取消选中 {role}: {name}")
            self.page.get_by_role(role, name=name).uncheck(timeout=self.timeout)
            self.logger.info(f"成功取消选中 {role}: {name}")
        except TimeoutError:
            self.logger.error(f"元素未找到: {role} - {name}")
            raise
        except Exception as e:
            self.logger.error(f"取消选中元素失败: {role} - {name}, 错误: {str(e)}")
            raise
