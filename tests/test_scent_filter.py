import random
import re

import pytest
from playwright.sync_api import expect, Page

from src.help_methods import get_random_int
from src.pages.home_page import HomePage
from src.pages.scent_page import ScentPage


@pytest.fixture(name="scent")
def get_scent(page: Page) -> ScentPage:
    return ScentPage(page)


@pytest.fixture(name="scent_page")
def get_scent_page(scent: ScentPage) -> ScentPage:
    return scent.open()


@pytest.fixture(name="random_preis_data")
def get_data() -> dict:
    start = get_random_int(minimum=1, maximum=800)
    end = get_random_int(minimum=801, maximum=1700)
    return {"preis-from": start, "preis-to": end}


class TestScent:

    def test_apply_input_facet(self, scent_page: ScentPage, random_preis_data):
        scent_page.click_show_more_less_filter()
        scent_page.price.apply_input_facet(**random_preis_data)
        scent_page.verify_applied_facets(
            f"{random_preis_data['preis-from']:,.2f} € bis {random_preis_data['preis-to']:,.2f} €"
        )

    def test_clear_filter(self, scent_page: ScentPage):
        facet = random.choice([
            scent_page.brand, scent_page.highlights, scent_page.product_feature, scent_page.product_type,
            scent_page.fragrance_note, scent_page.for_whom, scent_page.present_for, scent_page.scope_of_application])
        facet_name = facet.select_value()
        scent_page.remove_facet(facet_name)
        scent_page.verify_remove_facet(facet_name)

    def test_navigate_to_scent_page(self, page: Page, scent: ScentPage) -> None:
        home_page = HomePage(page)
        home_page.select_header_menu_item("PARFUM")

        expect(scent.page).to_have_title(scent.PAGE_TITLE)
        expect(scent.page).to_have_url(re.compile(".*/c/parfum/01"))

    def test_show_more_less_filter(self, scent_page: ScentPage):
        for _ in range(2):
            scent_page.click_show_more_less_filter()
            expect(scent_page.price.element).to_be_visible() if _ % 2 == 0 else expect(
                scent_page.price.element).not_to_be_visible()

    @pytest.mark.parametrize(
        "facet_name", [
            "product_type", "brand", "for_whom", "fragrance_note", "product_feature", "scope_of_application",
            "highlights", "present_for"
        ]
    )
    def test_apply_one_drop_down_facet(self, scent_page: ScentPage, facet_name: str):
        facet = getattr(scent_page, facet_name)
        value = facet.select_value()

        scent_page.verify_applied_facets(filter_names=value)

    @pytest.mark.parametrize("highlight", ("Sale", "NEU"))
    def test_case_1_and_2(self, scent_page: ScentPage, highlight):
        scent_page.highlights.select_value(value=highlight)
        brand = scent_page.brand.select_value()
        product_type = scent_page.product_type.select_value()
        for_whom = scent_page.for_whom.select_value()

        scent_page.verify_applied_facets(sorted([highlight, brand, product_type, for_whom]))
        expect(scent_page.present_for.element).not_to_be_visible()

    def test_case_3(self, scent_page: ScentPage):
        scent_page.highlights.select_value(value="Limitiert")
        brand = scent_page.brand.select_value()
        product_type = scent_page.product_type.select_value()
        present_for = scent_page.present_for.select_value()
        for_whom = scent_page.for_whom.select_value()

        scent_page.verify_applied_facets(sorted(["Limitiert", brand, product_type, present_for, for_whom]))
