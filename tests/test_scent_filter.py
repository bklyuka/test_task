import random
import re

import pytest
from playwright.sync_api import expect, Page

from src.components.facet import Facet
from src.help_methods import get_random_int
from src.pages.scent_page import ScentPage


@pytest.fixture(name="scent")
def get_scent(page: Page) -> ScentPage:
    return ScentPage(page)


@pytest.fixture(name="scent_page")
def get_scent_page(scent: ScentPage) -> ScentPage:
    return scent.open()


@pytest.fixture(name="random_price_data")
def generate_valid_random_price_data(scent_page: ScentPage) -> dict:
    scent_page.click_show_more_less_filter()
    scent_page.price.toggle()
    min_value = scent_page.price.get_input_value(scent_page.price.min)
    max_value = scent_page.price.get_input_value(scent_page.price.max)

    start = get_random_int(minimum=min_value + 1, maximum=max_value / 2)
    end = get_random_int(minimum=max_value / 2, maximum=max_value - 1)
    return {"preis-from": start, "preis-to": end}


class TestScent:

    @pytest.mark.parametrize(
        "menu_name, expected_title, expected_url",
        (
                ("MARKEN", "Make-Up & Parfum Marken ✔️ DOUGLAS", ".*de/brands"),
                ("PARFUM", "Parfüm & Düfte ✔️ online kaufen » für Sie & Ihn | DOUGLAS", ".*de/c/parfum/01"),
                ("MAKE-UP", "Make-up ✔️ online kaufen | DOUGLAS", ".*de/c/make-up/03"),
                ("GESICHT", "Gesichtspflege ✔️ online kaufen | DOUGLAS", ".*de/c/gesicht/12"),
                ("KÖRPER", "Körperpflege ✔️ online kaufen | DOUGLAS", ".*de/c/koerper/13"),
                ("HAARE", "Haarpflege: Shampoo, Conditioner & Co. ✔️ online kaufen | DOUGLAS", ".*de/c/haare/14"),
                ("HOME & LIFESTYLE", "Home & Lifestyle ✔️ online kaufen | DOUGLAS", ".*de/c/home-lifestyle/15"),
                ("DOUGLAS COLLECTION", "Douglas Collection ✔️ online kaufen | DOUGLAS", ".*de/b/douglas-collection/b9834"),
                ("OSTERN", "Ostergeschenke 2024 ✔️ online kaufen | DOUGLAS", ".*de/c/ostergeschenke/82"),
                ("SALE", "Beauty SALE ✔️ online entdecken bei DOUGLAS", ".*de/c/sale/05"),
                ("Nachhaltigkeit", "Nachhaltigkeit ✔️ online kaufen | DOUGLAS", ".*de/c/nachhaltigkeit/59"),
                ("LUXUS", "Douglas Luxuswelt ✔️ online kaufen | DOUGLAS", ".*de/c/luxuswelt/29"),
                ("NEU", "Kosmetik- und Beauty-Neuheiten ✔️ online kaufen | DOUGLAS", ".*de/c/neuheiten/09")
        )
    )
    def test_navigate_through_header_menu(
            self, scent_page: ScentPage, menu_name: str, expected_title: str, expected_url: str, page: Page
    ):
        scent_page.header.select_header_menu_item(menu_item_name=menu_name)
        expect(page).to_have_title(expected_title)
        expect(page).to_have_url(re.compile(f"{expected_url}"))

    def test_search_in_facet_with_valid_data(self, scent_page: ScentPage):
        searchable_facet = random.choice([
            scent_page.product_type, scent_page.brand, scent_page.fragrance_note, scent_page.product_feature,
            scent_page.scope_of_application, scent_page.present_for])

        name = random.choice(searchable_facet.get_all_values())
        searchable_facet.search_by_text(name)
        searchable_facet.verify_facet_menu_contains(name)

    def test_search_in_facet_with_invalid_data(self, scent_page: ScentPage):
        searchable_facet: Facet = random.choice([
            scent_page.product_type, scent_page.brand, scent_page.fragrance_note, scent_page.product_feature,
            scent_page.scope_of_application, scent_page.present_for])

        invalid = str(get_random_int())
        searchable_facet.search_by_text(invalid)
        searchable_facet.verify_facet_menu_does_not_contain(invalid)

    def test_apply_input_facet(self, scent_page: ScentPage, random_price_data):
        scent_page.price.apply_input_facet(**random_price_data)
        scent_page.verify_applied_facets(
            filter_names=f"{random_price_data['preis-from']:,.2f} € bis {random_price_data['preis-to']:,.2f} €"
        )

    def test_clear_filter(self, scent_page: ScentPage):
        facet = random.choice([
            scent_page.brand, scent_page.highlights, scent_page.product_feature, scent_page.product_type,
            scent_page.fragrance_note, scent_page.for_whom, scent_page.present_for, scent_page.scope_of_application])
        facet_name = facet.select_value()
        scent_page.remove_facet(facet_name)
        scent_page.verify_remove_facet(facet_name)

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
