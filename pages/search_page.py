from playwright.sync_api import Page
from config.config import TIMEOUT
from pages.base_page import BasePage
from config.config import BASE_URL
from utils.data_loader import DataLoader


class SearchPage(BasePage):
    SEARCH_TEXT = "#chat-textarea"
    SEARCH_BUTTON = "#chat-submit-button"


    def open(self):
        self.navigate(f"{BASE_URL}")

    def search(self, query: str):
        search_data = DataLoader.get_test_data("search_data.yaml", "search_data")
        self.page.fill(self.SEARCH_TEXT, query)
        self.page.click(self.SEARCH_BUTTON, )
        self.page.wait_for_selector("#search-results")
        return self.page.text_content("#search-results")