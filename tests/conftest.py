import pytest
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page

from src.pages.home_page import HomePage


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome", help="select browser: chrome or firefox")
    parser.addini("headless", default="False", help="Run tests without displaying UI of browser")


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="class")
def browser(request, playwright: Playwright):
    browser_name = request.config.getoption("--browser_name")
    headless = request.config.getini("headless") == 'True'

    if browser_name == "firefox":
        browser = playwright.firefox.launch(headless=headless)
    elif browser_name == "chrome":
        browser = playwright.chromium.launch(headless=headless)
    else:
        raise ValueError(f"Unsupported browser type `{browser_name}`. Supported types: chrome, firefox")
    yield browser
    browser.close()


@pytest.fixture(scope="class")
def context(browser: Browser):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="class")
def page(context: BrowserContext):
    page: Page = context.new_page()
    page.set_viewport_size({"width": 1920, "height": 1024})
    yield page
    page.close()


@pytest.fixture(scope="class", autouse=True)
def get_home_page(page):
    HomePage(page).open(close_cookie=True)
