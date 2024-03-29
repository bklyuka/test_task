from playwright.sync_api import Page


class Header:
    def __init__(self, page: Page):
        self.page = page
        self.menu_item = self.page.locator("div > li.navigation-main-entry > a")

    def select_header_menu_item(self, menu_item_name: str):
        menu_item = self.menu_item.filter(has_text=menu_item_name)
        if menu_item.is_visible():
            menu_item.click()
            self.page.wait_for_load_state()
        return self
