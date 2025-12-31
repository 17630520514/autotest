from pages.base_page import BasePage
from config.config import BASE_URL


class MarPage(BasePage):
    """用药记录页面"""

    # ========== Role 定位器 ==========
    MAR_TAB_BUTTON = ("button", "用药记录")
    ADD_MAR_BUTTON = ("button", "添加用药记录")
    MAR_NAME_INPUT = ("textbox", "药物名称 *")
    MAR_DOSAGE_INPUT = ("textbox", "剂量")
    MAR_FREQUENCY_INPUT = ("textbox", "用药频率")
    MAR_PURPOSE_INPUT = ("textbox", "用药目的")
    MAR_SIDE_EFFECTS_INPUT = ("textbox", "副作用")
    MAR_STILL_USING_INPUT = ("checkbox", "当前仍在使用")
    SAVE_MAR_BUTTON = ("button", "保存")

    def open(self):
        """打开页面（已登录状态下直接访问）"""
        self.navigate(f"{BASE_URL}")

    def click_mar(self):
        """点击用药记录tab按钮 - 新方式：直接传递元组"""
        # 不再需要 * 解包，直接传递定位器即可
        self.click(self.MAR_TAB_BUTTON)
        # 添加等待，确保页面加载完成
        self.page.wait_for_timeout(2000)
        self.click(self.ADD_MAR_BUTTON)

        # 检查复选框是否选中
        # checked_state = self.is_checked(self.MAR_STILL_USING_INPUT)
        # if not checked_state:
        #     self.check(self.MAR_STILL_USING_INPUT)
        # self.fill(self.MAR_NAME_INPUT, "测试药物")
        # self.fill(self.MAR_DOSAGE_INPUT, "10mg")
        # self.fill(self.MAR_FREQUENCY_INPUT, "每日一次")
        # self.fill(self.MAR_PURPOSE_INPUT, "测试目的")
        # self.fill(self.MAR_SIDE_EFFECTS_INPUT, "测试副作用")
        
        # self.click(self.SAVE_MAR_BUTTON)

    def get_mar_tab_text(self) -> str:
        """获取用药记录页面标题"""
        # 同样直接传递元组，get_text 会自动识别
        return self.get_text(self.MAR_TAB_BUTTON)
