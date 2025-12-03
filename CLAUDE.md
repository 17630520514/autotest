# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Web UI automation framework using Python + Playwright + Pytest with Page Object Model (POM) pattern.

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
pytest tests/test_login.py

# Run specific test method
pytest tests/test_login.py::TestLogin::test_login_success

# Run with different browser
pytest --browser firefox
pytest --browser webkit

# Run in headless mode
pytest --browser chromium --headless

# Run with verbose output
pytest -v

# Run with detailed output and logs
pytest -s -v
```

## Architecture

### Page Object Model Structure

The framework follows POM pattern with clear separation:

- **BasePage** (`pages/base_page.py`): Base class providing common page operations (navigate, click, fill, get_text, is_visible, wait_for_selector). All page objects inherit from this class. Uses centralized logging and timeout configuration.

- **Page Objects** (`pages/`): Each page class inherits from BasePage and defines page-specific locators and actions. Example: `LoginPage` encapsulates login page elements and login flow.

- **Test Data** (`test_data/`): YAML files containing test data. Accessed via `DataLoader.get_test_data(file_name, key)` which returns data from `test_data/` directory.

- **Configuration** (`config/config.py`): Centralized config for BASE_URL, TIMEOUT, HEADLESS mode, and logging settings.

- **Fixtures** (`conftest.py`): Pytest fixtures for browser setup. Session-scoped fixtures configure browser launch args and context args. Function-scoped `page` fixture provides fresh page instance per test.

### Key Patterns

- All page operations go through BasePage methods for consistent logging and error handling
- Test data is externalized in YAML files under `test_data/`
- Logger is initialized per class: `Logger(self.__class__.__name__)` or `Logger.get_logger("TestName")`
- Timeout is configured globally in `config.py` (default: 30000ms)
