from pages.base_page import BasePage
from config.config import BASE_URL


class MarPage(BasePage):
    """用药记录页面"""

    # 定位器
    MAR_TAB_BUTTON = "button >> nth=3"  # 第4个button（从0开始）
    # 或者使用更具体的定位方式：
    # MAR_TAB_BUTTON = "button:has-text('用药记录')"  # 根据按钮文本定位
    # MAR_TAB_BUTTON = "//button[contains(text(), '用药记录')]"  # XPath方式

    def open(self):
        """打开页面（已登录状态下直接访问）"""
        self.navigate(f"{BASE_URL}")

    def click_mar(self):
        """点击用药记录tab按钮"""
        self.click(self.MAR_TAB_BUTTON)
        
    def get_mar_tab_text(self) -> str:
        """获取用药记录页面标题"""
        return self.get_text(self.MAR_TAB_BUTTON)

    # def is_mar_page_displayed(self) -> bool:
    #     """验证用药记录页面是否显示"""
    #     # 根据实际页面情况，选择一个用药记录页面特有的元素来验证
    #     # 例如：
    #     # return self.is_visible("#mar-content")
    #     # 暂时返回 True，你需要根据实际页面调整
    #     return True
