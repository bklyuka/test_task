from typing import List, Union

from playwright.sync_api import Page, expect

from src.components.facet import Facet, FacetInput
from src.pages.base_page import BasePage


class ScentPage(BasePage):
    PAGE_TITLE = "Parfüm & Düfte ✔️ online kaufen » für Sie & Ihn | DOUGLAS"

    def __init__(self, page: Page):
        super().__init__(page)
        self.relative_url: str = "/c/parfum/01"

        self.filter = self.page.locator(".selected-facets__value")
        self.more_less_button = self.page.locator(".facet-list__show-more")

    @property
    def product_type(self) -> Facet:
        return Facet(page=self.page, name="Produktart")

    @property
    def brand(self) -> Facet:
        return Facet(page=self.page, name="Marke")

    @property
    def for_whom(self) -> Facet:
        return Facet(page=self.page, name="Für Wen")

    @property
    def fragrance_note(self) -> Facet:
        return Facet(page=self.page, name="Duftnote")

    @property
    def scope_of_application(self) -> Facet:
        return Facet(page=self.page, name="Anwendungsbereich")

    @property
    def product_feature(self) -> Facet:
        return Facet(page=self.page, name="Produktmerkmal")

    @property
    def highlights(self) -> Facet:
        return Facet(page=self.page, name="Highlights")

    @property
    def present_for(self) -> Facet:
        return Facet(page=self.page, name="Geschenk für")

    @property
    def price(self) -> FacetInput:
        return FacetInput(page=self.page, name="Preis")

    def click_show_more_less_filter(self):
        self.more_less_button.click()
        return self

    def verify_applied_facets(self, filter_names: Union[str, List[str]]):
        filter_names = [filter_names] if isinstance(filter_names, str) else filter_names

        for locator, filter_name in zip(self.filter.all(), filter_names):
            expect(locator).to_be_visible()
            expect(locator).to_have_text(filter_name)

    def verify_remove_facet(self, facet_name: str):
        expect(self.filter.filter(has_text=facet_name)).not_to_be_visible()

    def remove_facet(self, filter_name: str):
        self.filter.filter(has_text=filter_name).click()
        return self
