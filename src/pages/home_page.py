from playwright.sync_api import Page

from src.pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.filter = self.page.locator(".selected-facets__value")

