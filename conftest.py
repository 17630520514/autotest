import allure
import pytest
from playwright.sync_api import Page, Browser
from pathlib import Path
from config.config import HEADLESS, BASE_URL


# Storage state 文件路径
STORAGE_STATE_PATH = Path(__file__).parent / "test_data" / "auth_state.json"


@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {"headless": HEADLESS}


@pytest.fixture(scope="session")
def browser_context_args():
    return {"viewport": {"width": 1920, "height": 1080}}


@pytest.fixture(scope="session")
def authenticated_state(browser: Browser) -> Path:
    """
    Session级别的fixture，执行一次登录并保存认证状态
    其他测试可以复用这个状态，避免重复登录
    """
    # 如果已经有保存的状态文件，直接返回
    if STORAGE_STATE_PATH.exists():
        return STORAGE_STATE_PATH

    # 创建临时上下文进行登录
    context = browser.new_context()
    page = context.new_page()

    try:
        # 执行登录流程
        from pages.login.login_page import LoginPage
        from utils.data_loader import DataLoader

        login_data = DataLoader.get_test_data("login/login_data.yaml", "valid_user")
        login_page = LoginPage(page)
        login_page.open()
        login_page.login(login_data["username"], login_data["password"])

        # 等待登录成功（可以根据实际情况调整等待条件）
        page.wait_for_timeout(2000)

        # 保存认证状态
        STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        context.storage_state(path=str(STORAGE_STATE_PATH))

        print(f"✓ 登录状态已保存到: {STORAGE_STATE_PATH}")

    finally:
        context.close()

    return STORAGE_STATE_PATH


@pytest.fixture(scope="function")
def page(browser: Browser):
    """默认的page fixture，不带登录状态"""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def authenticated_page(browser: Browser, authenticated_state: Path):
    """
    带登录状态的page fixture
    使用方法：在测试函数参数中使用 authenticated_page 替代 page
    """
    context = browser.new_context(storage_state=str(authenticated_state))
    page = context.new_page()
    yield page
    context.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """在测试失败时自动截图并附加到 Allure 报告"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # 获取页面对象
        page = item.funcargs.get("page")
        if page:
            try:
                # 截图
                screenshot_bytes = page.screenshot(full_page=True)
                allure.attach(
                    screenshot_bytes,
                    name=f"失败截图_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )

                # 附加页面 URL
                allure.attach(
                    page.url,
                    name="页面URL",
                    attachment_type=allure.attachment_type.TEXT
                )
            except Exception as e:
                print(f"截图失败: {e}")
