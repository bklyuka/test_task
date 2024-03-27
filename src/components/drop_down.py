import random

from playwright.sync_api import Page, Locator, expect


class DropDown:
    EXPANDED_MENU: str = ".rc-scrollbars-view"

    def __init__(self, page: Page, name):
        self.page: Page = page
        self.name: str = name
        self._element: Locator = page.locator(selector=".facet-wrapper .facet__title", has_text=self.name)

    @property
    def element(self) -> Locator:
        return self._element

    def toggle(self):
        if self.page.locator(".rc-scrollbars-view").is_hidden():
            self._element.click()
            self.page.wait_for_selector(selector=self.EXPANDED_MENU, state="visible")
        else:
            self._element.click()
            self.page.wait_for_selector(selector=self.EXPANDED_MENU, state="hidden")
        return self

    def select_value(self, value: str = None):
        self.toggle()
        if value is None:
            value = random.choice(self.page.locator(selector=".facet__menu a").all_inner_texts())
        self.page.get_by_role(role="checkbox", name=value, exact=True).click()
        expect(self.page.locator(selector=".facet__menu a", has_text=value)).to_be_checked()
        self.toggle()
        return value
