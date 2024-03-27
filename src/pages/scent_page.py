from typing import List, Union

from playwright.sync_api import Page, expect

from src.components.drop_down import DropDown
from src.pages.base_page import BasePage


class ScentPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.relative_url: str = "/c/parfum/01"

        self.filter = self.page.locator(".selected-facets__value")

    @property
    def product_type(self) -> DropDown:
        return DropDown(page=self.page, name="Produktart")

    @property
    def brand(self) -> DropDown:
        return DropDown(page=self.page, name="Marke")

    @property
    def for_whom(self) -> DropDown:
        return DropDown(page=self.page, name="Für Wen")

    @property
    def product_feature(self) -> DropDown:
        return DropDown(page=self.page, name="Produktmerkmal")

    @property
    def highlights(self) -> DropDown:
        return DropDown(page=self.page, name="Highlights")

    @property
    def present_for(self) -> DropDown:
        return DropDown(page=self.page, name="Geschenk für")

    # def verify_applied_filters(self, filter_names: List[str]):
    #     for locator, filer_name in zip(self.filter.all(), filter_names):
    #         expect(locator).to_be_visible()
    #         expect(locator).to_have_text(filer_name)

    def verify_applied_filters(self, filter_names: Union[str, List[str]]):
        if isinstance(filter_names, str):
            filter_names = [filter_names]

        for locator, filter_name in zip(self.filter.all(), filter_names):
            expect(locator).to_be_visible()
            expect(locator).to_have_text(filter_name)
