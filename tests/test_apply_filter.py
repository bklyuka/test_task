import pytest
from playwright.sync_api import expect

from src.pages.scent_page import ScentPage


@pytest.fixture(name="scent_page")
def get_scent_page(page) -> ScentPage:
    return ScentPage(page).open()


class TestFilters:

    @pytest.mark.parametrize(
        "facet_name", ["product_type", "brand", "for_whom", "product_feature", "highlights", "present_for"]
    )
    def test_apply_one_facet(self, scent_page: ScentPage, facet_name):
        facet = getattr(scent_page, facet_name)
        value = facet.select_value()

        scent_page.verify_applied_filters(filter_names=value)

    # def test_case_1(self, scent_page: ScentPage):
    #     scent_page.highlights.select_value(value='Sale')
    #     brand = scent_page.brand.select_value()
    #     product_type = scent_page.product_type.select_value()
    #     for_whom = scent_page.for_whom.select_value()
    #
    #     scent_page.verify_applied_filters(sorted(['Sale', brand, product_type, for_whom]))
    #     expect(scent_page.present_for.element).not_to_be_visible()
    #
    # def test_case_2(self, scent_page: ScentPage):
    #     scent_page.highlights.select_value(value='NEU')
    #     brand = scent_page.brand.select_value()
    #     product_type = scent_page.product_type.select_value()
    #     for_whom = scent_page.for_whom.select_value()
    #
    #     scent_page.verify_applied_filters(sorted(['NEU', brand, product_type, for_whom]))
    #     expect(scent_page.present_for.element).not_to_be_visible()

    @pytest.mark.parametrize("highlight", ("Sale", "NEU"))
    def test_case_1_and_2(self, scent_page: ScentPage, highlight):
        scent_page.highlights.select_value(value=highlight)
        brand = scent_page.brand.select_value()
        product_type = scent_page.product_type.select_value()
        for_whom = scent_page.for_whom.select_value()

        scent_page.verify_applied_filters(sorted([highlight, brand, product_type, for_whom]))
        expect(scent_page.present_for.element).not_to_be_visible()

    def test_case_3(self, scent_page: ScentPage):
        scent_page.highlights.select_value(value="Limitiert")
        brand = scent_page.brand.select_value()
        product_type = scent_page.product_type.select_value()
        present_for = scent_page.present_for.select_value()
        for_whom = scent_page.for_whom.select_value()

        scent_page.verify_applied_filters(sorted(["Limitiert", brand, product_type, present_for, for_whom]))
