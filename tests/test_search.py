import allure
import pytest
from playwright.sync_api import Page
from config.config import BASE_URL


@allure.feature("搜索功能")
class TestSearch:
    """
    搜索功能测试 - 需要登录后才能使用
    使用 authenticated_page 替代 page，自动加载登录状态
    """

    @allure.story("搜索关键词")
    @allure.title("测试搜索功能")
    @allure.description("使用已登录的状态进行搜索操作")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_with_keyword(self, authenticated_page: Page):
        """
        使用 authenticated_page 参数，会自动加载登录状态
        不需要再执行登录操作
        """
        # 直接访问需要登录的页面
        authenticated_page.goto(BASE_URL)

        # 这里可以直接进行搜索操作，因为已经是登录状态
        # 示例：假设有搜索框
        # search_input = authenticated_page.locator("#search")
        # search_input.fill("测试关键词")
        # search_input.press("Enter")

        # 验证搜索结果
        authenticated_page.wait_for_timeout(1000)
        print("✓ 搜索功能测试完成（已自动登录）")

    @allure.story("搜索历史")
    @allure.title("测试查看搜索历史")
    @allure.description("查看用户的搜索历史记录")
    @allure.severity(allure.severity_level.MINOR)
    def test_search_history(self, authenticated_page: Page):
        """
        第二个测试也使用 authenticated_page
        会复用之前保存的登录状态，不会重新登录
        """
        authenticated_page.goto(BASE_URL)

        # 这里可以测试搜索历史功能
        # 示例：
        # authenticated_page.click("#search-history")
        # assert authenticated_page.is_visible("#history-list")

        print("✓ 搜索历史测试完成（复用登录状态）")
