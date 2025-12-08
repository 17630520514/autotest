import allure
import pytest
from playwright.sync_api import Browser
from pathlib import Path
from config.config import HEADLESS, BASE_URL
import time
import os


# Storage state 文件路径
STORAGE_STATE_PATH = Path(__file__).parent / "test_data" / "auth_state.json"

# 认证状态有效期（秒），超过此时间将重新登录
# 可根据实际 token 过期时间调整，默认 1 小时
AUTH_STATE_EXPIRY = 60 * 60  # 1 hour

# Trace 文件保存路径
TRACE_DIR = Path(__file__).parent / "test-results"


def pytest_addoption(parser):
    """添加自定义命令行选项"""
    parser.addoption(
        "--trace-mode",
        action="store",
        default="off",
        help="启用 Playwright tracing: 'on' 所有测试, 'retain-on-failure' 仅失败测试保留, 'off' 禁用 (默认)"
    )


@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {"headless": HEADLESS}


@pytest.fixture(scope="session")
def browser_context_args():
    """配置浏览器上下文参数"""
    return {"viewport": {"width": 1920, "height": 1080}}


def _is_auth_state_valid(browser: Browser) -> bool:
    """
    验证保存的认证状态是否仍然有效
    通过尝试访问需要认证的页面并检查关键元素来判断
    """
    if not STORAGE_STATE_PATH.exists():
        return False

    try:
        # 创建使用保存状态的临时上下文
        context = browser.new_context(storage_state=str(STORAGE_STATE_PATH))
        page = context.new_page()

        # 访问主页
        page.goto(BASE_URL, timeout=10000)
        page.wait_for_timeout(1000)

        # 检查是否存在登录后才有的元素（如"用药记录"按钮）
        # 如果找到该元素，说明认证有效；否则可能跳转到了登录页
        try:
            page.wait_for_selector("button:has-text('用药记录')", timeout=5000)
            context.close()
            return True
        except:
            context.close()
            return False

    except Exception as e:
        print(f"⚠ 验证认证状态失败: {e}")
        return False


def _perform_login(browser: Browser) -> Path:
    """
    执行登录并保存认证状态
    """
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

        # 等待登录成功 - 等待特定元素出现确保登录完成
        try:
            page.wait_for_selector("button:has-text('用药记录')", timeout=5000)
            print("✓ 登录成功，已检测到主页元素")
        except:
            print("⚠ 警告：未检测到登录后的主页元素，但继续保存状态")
            page.wait_for_timeout(2000)

        # 保存认证状态
        STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        context.storage_state(path=str(STORAGE_STATE_PATH))

        print(f"✓ 登录状态已保存到: {STORAGE_STATE_PATH}")

    finally:
        context.close()

    return STORAGE_STATE_PATH


@pytest.fixture(scope="session")
def authenticated_state(browser: Browser) -> Path:
    """
    Session级别的fixture，执行一次登录并保存认证状态
    其他测试可以复用这个状态，避免重复登录

    自动检测功能：
    1. 检查文件是否存在
    2. 检查文件是否过期（基于修改时间）
    3. 验证认证状态是否有效（尝试访问需要认证的页面）
    4. 如果无效或过期，自动重新登录
    """
    need_refresh = False

    # 检查1：文件是否存在
    if not STORAGE_STATE_PATH.exists():
        print("ℹ 认证状态文件不存在，需要登录")
        need_refresh = True

    # 检查2：文件是否过期（基于修改时间）
    elif time.time() - os.path.getmtime(STORAGE_STATE_PATH) > AUTH_STATE_EXPIRY:
        print(f"ℹ 认证状态文件已过期（超过 {AUTH_STATE_EXPIRY/3600} 小时），需要重新登录")
        need_refresh = True

    # 检查3：验证认证状态是否有效
    elif not _is_auth_state_valid(browser):
        print("ℹ 认证状态已失效，需要重新登录")
        need_refresh = True
    else:
        print("✓ 使用现有有效的认证状态")

    # 如果需要刷新，删除旧文件并重新登录
    if need_refresh:
        if STORAGE_STATE_PATH.exists():
            STORAGE_STATE_PATH.unlink()
        return _perform_login(browser)

    return STORAGE_STATE_PATH


@pytest.fixture(scope="function")
def page(browser: Browser, request):
    """默认的page fixture，不带登录状态"""
    tracing_option = request.config.getoption("--trace-mode")

    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()

    # 启动 tracing
    if tracing_option in ["on", "retain-on-failure"]:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield page

    # 停止并保存 tracing
    if tracing_option in ["on", "retain-on-failure"]:
        # 获取测试结果
        test_failed = hasattr(request.node, 'rep_call') and request.node.rep_call.failed

        # 根据策略决定是否保存 trace
        should_save = (tracing_option == "on") or (tracing_option == "retain-on-failure" and test_failed)

        if should_save:
            TRACE_DIR.mkdir(parents=True, exist_ok=True)
            trace_path = TRACE_DIR / f"{request.node.name}.zip"
            context.tracing.stop(path=str(trace_path))

            # 附加到 Allure 报告
            if trace_path.exists():
                allure.attach.file(
                    str(trace_path),
                    name="Playwright Trace",
                    extension="zip"
                )
        else:
            context.tracing.stop()

    context.close()


@pytest.fixture(scope="function")
def authenticated_page(browser: Browser, authenticated_state: Path, request):
    """
    带登录状态的page fixture
    使用方法：在测试函数参数中使用 authenticated_page 替代 page
    """
    tracing_option = request.config.getoption("--trace-mode")

    context = browser.new_context(
        storage_state=str(authenticated_state),
        viewport={"width": 1920, "height": 1080}
    )
    page = context.new_page()

    # 启动 tracing
    if tracing_option in ["on", "retain-on-failure"]:
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield page

    # 停止并保存 tracing
    if tracing_option in ["on", "retain-on-failure"]:
        # 获取测试结果
        test_failed = hasattr(request.node, 'rep_call') and request.node.rep_call.failed

        # 根据策略决定是否保存 trace
        should_save = (tracing_option == "on") or (tracing_option == "retain-on-failure" and test_failed)

        if should_save:
            TRACE_DIR.mkdir(parents=True, exist_ok=True)
            trace_path = TRACE_DIR / f"{request.node.name}.zip"
            context.tracing.stop(path=str(trace_path))

            # 附加到 Allure 报告
            if trace_path.exists():
                allure.attach.file(
                    str(trace_path),
                    name="Playwright Trace",
                    extension="zip"
                )
        else:
            context.tracing.stop()

    context.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):  # noqa: ARG001
    """在测试失败时自动截图并附加到 Allure 报告，同时保存测试结果用于 tracing 判断"""
    outcome = yield
    report = outcome.get_result()

    # 保存测试结果到 item，供 fixture 使用
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        # 获取页面对象（支持 page 和 authenticated_page）
        page = item.funcargs.get("page") or item.funcargs.get("authenticated_page")
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
