import pytest
from playwright.sync_api import sync_playwright, Playwright, Browser, BrowserContext, Page

from src.pages.home_page import HomePage


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name",
        action="store",
        default="chrome",
        help="select browser: chrome or firefox"
    )


@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as pw:
        yield pw


@pytest.fixture(scope="class")
def browser(request, playwright: Playwright):
    browser_name = request.config.getoption("--browser_name")
    if browser_name == "firefox":
        browser = playwright.firefox.launch(headless=False)
    elif browser_name == "chrome":
        browser = playwright.chromium.launch(headless=False)
    else:
        raise ValueError("Unsupported browser type. Supported types: chrome, firefox")
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
