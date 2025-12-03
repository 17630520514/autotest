import pytest
from playwright.sync_api import Page, Browser
from config.config import HEADLESS


@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {"headless": HEADLESS}


@pytest.fixture(scope="session")
def browser_context_args():
    return {"viewport": {"width": 1920, "height": 1080}}


@pytest.fixture(scope="function")
def page(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
