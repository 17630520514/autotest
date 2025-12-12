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