# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Web UI automation framework using Python + Playwright + Pytest with Page Object Model (POM) pattern.

## Core Conventions and Key Information

This section highlights the most important information Claude Code should follow when working with this codebase.

### 🔴 Critical Rules (Must Follow)

1. **Always Use `Assertion` Class** - Never use native `assert`
   ```python
   from utils.assertion import Assertion
   assertion = Assertion()
   assertion.assert_equal(actual, expected, "Verify login success")
   ```

2. **Choose Correct Page Fixture**
   - Tests WITHOUT login: `def test_foo(self, page: Page):`
   - Tests WITH login: `def test_foo(self, authenticated_page: Page):`

3. **Follow Modular Structure** - When adding new feature module (e.g., "reports"):
   - `pages/reports/reports_page.py` - Page object class
   - `tests/reports/test_reports.py` - Test cases
   - `test_data/reports/reports_data.yaml` - Test data (if needed)

4. **All Pages Inherit from BasePage**
   ```python
   from pages.base_page import BasePage

   class ReportsPage(BasePage):
       def __init__(self, page):
           super().__init__(page)
   ```

### 🟡 Important Patterns

5. **Load Test Data via DataLoader**
   ```python
   from utils.data_loader import DataLoader
   # Path is relative to test_data/ directory
   data = DataLoader.get_test_data("login/login_data.yaml", "valid_user")
   ```

6. **Initialize Logger per Class**
   ```python
   from utils.logger import Logger
   self.logger = Logger(self.__class__.__name__)
   ```

7. **Use Allure Decorators**
   ```python
   @allure.feature("Login Module")
   class TestLogin:
       @allure.story("Successful Login")
       @allure.title("Test login with valid credentials")
       @allure.severity(allure.severity_level.CRITICAL)
       def test_login_success(self, authenticated_page: Page):
           pass
   ```

### 🟢 Quick Reference

8. **Common Test Commands**
   ```bash
   pytest                                    # Run all tests
   pytest tests/login/test_login.py          # Run specific file
   pytest --browser firefox                  # Use different browser
   pytest --trace-mode=retain-on-failure     # Save trace on failure
   allure serve allure-results               # View test report
   ```

9. **Configuration Location**
   - Global config: `config/config.py` (BASE_URL, TIMEOUT, HEADLESS)
   - Pytest config: `pytest.ini`
   - Fixtures: `conftest.py`

10. **Authentication State**
    - Login state saved to: `test_data/auth_state.json`
    - Reset login: Delete `auth_state.json` file
    - First run: Login executes once and saves state
    - Subsequent runs: State is loaded automatically

## Setup Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## Running Tests

```bash
# Run all tests (default: chromium, headed mode per pytest.ini)
pytest

# Run specific test file
pytest tests/login/test_login.py

# Run specific test method
pytest tests/login/test_login.py::TestLogin::test_login_success

# Run all tests in a module
pytest tests/login/

# Run with different browser
pytest --browser firefox
pytest --browser webkit

# Run in headless mode
pytest --browser chromium --headless

# Run with verbose output
pytest -v

# Run with detailed output and logs
pytest -s -v

# Run with Playwright tracing enabled
pytest --trace-mode=on                    # Enable tracing for all tests
pytest --trace-mode=retain-on-failure     # Only save traces for failed tests
pytest --trace-mode=off                   # Disable tracing (default)
```

## Playwright Tracing

The framework supports Playwright's trace feature via pytest-playwright plugin for detailed test execution analysis.

### Usage

```bash
# Enable tracing for all tests
pytest --trace-mode=on

# Only save traces for failed tests (recommended)
pytest --trace-mode=retain-on-failure

# Disable tracing (default)
pytest --trace-mode=off
```

### What's Included in Traces

- Screenshots at each step
- DOM snapshots
- Network activity
- Console logs
- Action timeline (clicks, inputs, navigations)
- Source code

### Viewing Traces

```bash
# Traces are saved to test-results/ directory
# View a trace using Playwright's trace viewer
playwright show-trace test-results/<test-name>.zip

# Or open trace viewer and drag-drop the .zip file
playwright show-trace
```

### Integration with Allure

- Trace files are automatically attached to Allure reports as ZIP files
- Failed tests include both screenshots and trace files
- Download and view traces directly from Allure report

## Allure Reports

The framework is integrated with Allure for comprehensive test reporting.

```bash
# Run tests (allure-results will be generated automatically per pytest.ini)
pytest

# Generate and open Allure report
allure serve allure-results

# Generate Allure report to specific directory
allure generate allure-results -o allure-report --clean

# Open existing report
allure open allure-report
```

### Allure Report Features

- Automatic screenshots on test failure
- Step-by-step execution tracking via `@allure.step` decorators
- Test categorization with `@allure.feature` and `@allure.story`
- Assertion results with detailed pass/fail information
- Page URL capture on failures
- Test severity levels and descriptions

## Architecture

### File Organization

The framework follows a **modular structure** where each feature/module has its own directory containing pages, tests, and test data:

```
autotest/
├── pages/                    # Page Objects
│   ├── base_page.py         # Base class for all pages
│   ├── login/               # Login module
│   │   └── login_page.py
│   └── mar/                 # MAR (Medication) module
│       └── mar_page.py
├── tests/                    # Test cases
│   ├── login/
│   │   └── test_login.py
│   └── mar/
│       └── test_mar.py
├── test_data/               # Test data (YAML)
│   ├── login/
│   │   └── login_data.yaml
│   └── auth_state.json      # Saved login state (gitignored)
├── utils/                   # Utilities
│   ├── assertion.py         # Assertion wrapper with Allure
│   ├── data_loader.py       # YAML data loader
│   └── logger.py            # Logging utility
├── config/
│   └── config.py           # Configuration
└── conftest.py             # Pytest fixtures

```

**Organizing New Modules**:
When adding a new feature module (e.g., "reports"), create:
- `pages/reports/reports_page.py` - Page object
- `tests/reports/test_reports.py` - Test cases
- `test_data/reports/reports_data.yaml` - Test data (if needed)

### Page Object Model Structure

The framework follows POM pattern with clear separation:

- **BasePage** (`pages/base_page.py`): Base class providing common page operations (navigate, click, fill, get_text, is_visible, wait_for_selector). All page objects inherit from this class. Uses centralized logging and timeout configuration. All methods are decorated with `@allure.step` for report tracking.

- **Page Objects** (`pages/{module}/`): Each page class inherits from BasePage and defines page-specific locators and actions. Organized by module (e.g., `pages/login/login_page.py`, `pages/mar/mar_page.py`). Each page encapsulates elements and actions for a specific page or feature.

- **Test Data** (`test_data/`): YAML files containing test data, organized by module. Accessed via `DataLoader.get_test_data(file_path, key)` where `file_path` is relative to `test_data/` directory (e.g., `"login/login_data.yaml"`).
  ```python
  # Load data from test_data/login/login_data.yaml
  data = DataLoader.get_test_data("login/login_data.yaml", "valid_user")
  ```

- **Configuration** (`config/config.py`): Centralized config for BASE_URL, TIMEOUT, HEADLESS mode, and logging settings.

- **Fixtures** (`conftest.py`): Pytest fixtures for browser setup. Session-scoped fixtures configure browser launch args and context args. Function-scoped `page` fixture provides fresh page instance per test. Includes `pytest_runtest_makereport` hook for automatic screenshot capture on test failure.

  - `page`: 默认的 page fixture，每个测试独立的浏览器上下文（无登录状态）
  - `authenticated_page`: 带登录状态的 page fixture，自动加载保存的登录状态
  - `authenticated_state`: Session级别的 fixture，在整个测试会话开始时执行一次登录并保存状态到 `test_data/auth_state.json`

- **Assertion** (`utils/assertion.py`): Assertion wrapper class that integrates with Allure. Provides methods like:
  - `assert_equal`, `assert_not_equal` - Value comparison
  - `assert_contains`, `assert_not_contains` - String/collection checks
  - `assert_true`, `assert_false` - Boolean checks
  - `assert_is_display`, `assert_not_display` - Element visibility (requires `page` parameter)
  - `assert_greater`, `assert_less` - Numeric comparison
  - `assert_in` - List membership

  All assertions automatically log to Allure with pass/fail status and detailed information.

### Key Patterns

- All page operations go through BasePage methods for consistent logging and error handling
- Use `Assertion` class instead of native `assert` for better reporting: `assertion.assert_equal(actual, expected, "message")`
- Test data is externalized in YAML files under `test_data/`
- Logger is initialized per class: `Logger(self.__class__.__name__)` or `Logger.get_logger("TestName")`
- Timeout is configured globally in `config.py` (default: 30000ms)
- Test classes use `@allure.feature()` and test methods use `@allure.story()`, `@allure.title()`, `@allure.description()`, and `@allure.severity()` decorators

### Authentication State Management

**Problem**: Most tests require login, but repeating login in every test is slow and redundant.

**Solution**: Use Storage State to save and reuse login state:

1. **For tests that DON'T need login**: Use `page` fixture (default)
   ```python
   def test_public_page(self, page: Page):
       page.goto("http://example.com")
   ```

2. **For tests that NEED login**: Use `authenticated_page` fixture
   ```python
   def test_user_dashboard(self, authenticated_page: Page):
       authenticated_page.goto("http://example.com/dashboard")
       # Already logged in, no need to login again
   ```

3. **How it works**:
   - First time: `authenticated_state` fixture executes login once and saves state to `test_data/auth_state.json`
   - Subsequent tests: `authenticated_page` loads the saved state instantly
   - Result: Login happens only once per test session

4. **Reset login state**: Delete `test_data/auth_state.json` to force fresh login
