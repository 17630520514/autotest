from pages.base_page import BasePage
from config.config import BASE_URL
from typing import Optional


class BloodEntryPage(BasePage):
    """血常规录入页面对象"""

    # ========== Role 定位器（元组格式）==========
    BLOOD_ENTRY_BUTTON = ("button", "血常规录入")
    SUBMIT_BUTTON = ("button", "开始AI智能分析")

    # ========== CSS 定位器（字符串格式）==========
    PLT_INPUT = "#plt"
    WBC_INPUT = "#wbc"
    RBC_INPUT = "#rbc"
    HGB_INPUT = "#hgb"
    TEST_DATE_INPUT = "#test_date"
    ERROR_MESSAGE = '[class = "text-sm mt-1 text-red-800"]'
    SUCCESS_MESSAGE = '[class = "text-sm mt-1 text-green-800"]'

    def open(self):
        """打开血常规页面"""
        self.navigate(f"{BASE_URL}")

    def click_blood_entry_button(self):
        """点击血常规录入按钮 - 使用 Role 定位器"""
        # 新方式：直接传递元组，不需要 * 解包
        self.click(self.BLOOD_ENTRY_BUTTON)

    def fill_blood_data(self, plt: str = "", wbc: str = "", rbc: str = "", hgb: str = "", test_date: Optional[str] = None):
        """填充血常规数据 - 使用 CSS 定位器

        Args:
            plt: 血小板计数
            wbc: 白细胞计数
            rbc: 红细胞计数
            hgb: 血红蛋白
            test_date: 检测日期 (可选), 格式: YYYY-MM-DD
        """
        # CSS 定位器也直接传递，方法会自动识别
        if plt:
            self.fill(self.PLT_INPUT, plt)
        if wbc:
            self.fill(self.WBC_INPUT, wbc)
        if rbc:
            self.fill(self.RBC_INPUT, rbc)
        if hgb:
            self.fill(self.HGB_INPUT, hgb)
        if test_date:
            self.fill(self.TEST_DATE_INPUT, test_date)

    def submit_blood_data(self):
        """提交血常规数据 - 使用 Role 定位器"""
        self.click(self.SUBMIT_BUTTON)

    def submit_blood_entry(self, plt: str = "", wbc: str = "", rbc: str = "", hgb: str = "", test_date: Optional[str] = None):
        """完整流程：点击录入按钮 -> 填充数据 -> 提交

        Args:
            plt: 血小板计数
            wbc: 白细胞计数
            rbc: 红细胞计数
            hgb: 血红蛋白
            test_date: 检测日期 (可选), 格式: YYYY-MM-DD
        """
        self.click_blood_entry_button()
        self.fill_blood_data(plt, wbc, rbc, hgb, test_date)
        self.submit_blood_data()

    def get_error_message(self) -> str:
        """获取错误消息文本 - 使用 CSS 定位器"""
        return self.get_text(self.ERROR_MESSAGE)

    def get_success_message(self) -> str:
        """获取成功消息文本 - 使用 CSS 定位器"""
        return self.get_text(self.SUCCESS_MESSAGE)

    def is_error_message_visible(self) -> bool:
        """检查错误消息是否可见 - 使用 CSS 定位器"""
        return self.is_visible(self.ERROR_MESSAGE)

    def is_success_message_visible(self) -> bool:
        """检查成功消息是否可见 - 使用 CSS 定位器"""
        return self.is_visible(self.SUCCESS_MESSAGE)


