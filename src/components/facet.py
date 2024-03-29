import random

from playwright.sync_api import Page, Locator, expect


class Facet:
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


class FacetInput(Facet):
    EXPANDED_MENU = ".facet__menu-content"

    def __init__(self, page: Page, name):
        super().__init__(page, name)

    def select_value(self, value: str = None):
        raise NotImplementedError("Not available for FacetInput")

    def populate_input(self, **kwargs):
        for name, value in kwargs.items():
            self.page.get_by_test_id(test_id=name).fill(str(value))
        return self

    def apply_input_facet(self, **kwargs):
        self.toggle()
        self.populate_input(**kwargs)
        self.page.locator(selector=".facet-slider__close-button", has_text="Speichern").click()
        return self
