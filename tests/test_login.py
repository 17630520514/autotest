from sre_parse import SUCCESS
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from utils.data_loader import DataLoader
from utils.logger import Logger
logger = Logger.get_logger("TestLogin")


class TestLogin:
    def test_login_success(self, page: Page):
        success_data = DataLoader.get_test_data("login_data.yaml", "valid_user")
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(success_data["username"], success_data["password"])
        # page.wait_for_timeout(5000)
        success = login_page.get_success_message()
        assert success == success_data["expected_success"]

    def test_login_invalid_credentials(self, page: Page):
        invalid_data = DataLoader.get_test_data("login_data.yaml", "invalid_user")
        logger.debug(f"测试数据: {invalid_data}")
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(invalid_data["username"], invalid_data["password"])
        # page.wait_for_timeout(5000)
        error = login_page.get_error_message()
        assert invalid_data["expected_error"] in error
        

        
