from playwright.sync_api import Page

from src.pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.filter = self.page.locator(".selected-facets__value")

    def select_header_menu_item(self, header_name: str):
        self.page.locator(selector="li", has_text=header_name).click()
        return self
