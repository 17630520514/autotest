import allure
from playwright.sync_api import Page, TimeoutError
from config.config import TIMEOUT
from utils.logger import Logger


class BasePage:
    """页面基类,封装通用的页面操作方法"""

    def __init__(self, page: Page):
        self.page = page
        self.timeout = TIMEOUT
        self.logger = Logger(self.__class__.__name__)

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

    @allure.step("点击元素: {selector}")
    def click(self, selector: str):
        """点击元素"""
        try:
            self.logger.info(f"尝试点击元素: {selector}")
            self.page.click(selector, timeout=self.timeout)
            self.logger.info(f"成功点击元素: {selector}")
        except TimeoutError:
            self.logger.error(f"元素未找到或不可点击: {selector}")
            raise
        except Exception as e:
            self.logger.error(f"点击元素失败: {selector}, 错误: {str(e)}")
            raise

    @allure.step("填充元素: {selector}, 内容: {text}")
    def fill(self, selector: str, text: str):
        """填充输入框"""
        try:
            self.logger.info(f"尝试填充元素: {selector}, 内容: {text}")
            self.page.fill(selector, text, timeout=self.timeout)
            self.logger.info(f"成功填充元素: {selector}")
        except TimeoutError:
            self.logger.error(f"输入框未找到: {selector}")
            raise
        except Exception as e:
            self.logger.error(f"填充元素失败: {selector}, 错误: {str(e)}")
            raise

    @allure.step("获取元素文本: {selector}")
    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        try:
            self.logger.info(f"尝试获取元素文本: {selector}")
            text = self.page.text_content(selector, timeout=self.timeout)
            self.logger.info(f"成功获取文本: {selector}, 内容: {text}")
            return text
        except TimeoutError:
            self.logger.error(f"元素未找到,无法获取文本: {selector}")
            raise
        except Exception as e:
            self.logger.error(f"获取文本失败: {selector}, 错误: {str(e)}")
            raise

    @allure.step("检查元素可见性: {selector}")
    def is_visible(self, selector: str) -> bool:
        """检查元素是否可见"""
        try:
            visible = self.page.is_visible(selector)
            if visible:
                self.logger.info(f"元素可见: {selector}")
            else:
                self.logger.warning(f"元素不可见: {selector}")
            return visible
        except Exception as e:
            self.logger.error(f"检查元素可见性失败: {selector}, 错误: {str(e)}")
            return False

    @allure.step("等待元素出现: {selector}")
    def wait_for_selector(self, selector: str):
        """等待元素出现"""
        try:
            self.logger.info(f"等待元素出现: {selector}")
            self.page.wait_for_selector(selector, timeout=self.timeout)
            self.logger.info(f"元素已出现: {selector}")
        except TimeoutError:
            self.logger.error(f"等待超时,元素未出现: {selector}")
            raise
        except Exception as e:
            self.logger.error(f"等待元素失败: {selector}, 错误: {str(e)}")
            raise
