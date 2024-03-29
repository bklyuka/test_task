import random
from typing import List

from playwright.sync_api import Page, Locator, expect


class Facet:
    EXPANDED_MENU: str = ".rc-scrollbars-view"

    def __init__(self, page: Page, name):
        self.page: Page = page
        self.name: str = name
        self._element: Locator = page.locator(selector=".facet-wrapper .facet__title", has_text=self.name)
        self.item = self.page.locator(".facet__menu a")

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
            value = random.choice(self.item.all_inner_texts())
        self.page.get_by_role(role="checkbox", name=value, exact=True).click()
        expect(self.page.locator(selector=".facet__menu a", has_text=value)).to_be_checked()
        self.toggle()
        return value

    def get_all_values(self) -> List[str]:
        self.toggle()
        data = self.item.all_inner_texts()
        self.toggle()
        return data

    def search_by_text(self, text: str):
        self.toggle()
        self.page.locator(".facet__menu").locator(".input__input").fill(text)
        return self

    def verify_facet_menu_contains(self, value):
        expect(self.item).to_contain_text([value])

    def verify_facet_menu_does_not_contain(self, value):
        expect(self.item).not_to_contain_text([value])


class FacetInput(Facet):
    EXPANDED_MENU = ".facet__menu-content"
    MIN = "preis-from"
    MAX = "preis-to"

    def __init__(self, page: Page, name):
        super().__init__(page, name)
        self.min = self.MIN
        self.max = self.MAX

    def select_value(self, value: str = None):
        raise NotImplementedError("Not available for FacetInput")

    def populate_input(self, **kwargs):
        for name, value in kwargs.items():
            self.page.get_by_test_id(test_id=name).fill(str(value))
        return self

    def apply_input_facet(self, **kwargs):
        self.populate_input(**kwargs)
        self.page.locator(selector=".facet-slider__close-button", has_text="Speichern").click()
        return self

    def get_input_value(self, test_id) -> int:
        return int(self.page.get_by_test_id(test_id=test_id).get_attribute(name="value"))
