from typing import Optional
from urllib.parse import urljoin

from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page: Page = page
        self.base_url: str = "https://www.douglas.de/de"
        self.relative_url: Optional[str] = None

    def open(self, close_cookie: bool = False):
        url = urljoin(self.base_url, self.relative_url) if self.relative_url else self.base_url
        self.page.goto(url=url)
        if close_cookie:
            self.page.get_by_role(role="button", name="Alle erlauben").click()
        self.page.wait_for_load_state()
        return self

    # def open(self):
    #     url = urljoin(self.base_url, self.relative_url) if self.relative_url else self.base_url
    #     self.page.goto(url=url)
    #     self.page.add_locator_handler(
    #         self.page.get_by_role(role="dialog"),
    #         lambda: self.page.get_by_role(role="button", name="Alle erlauben").click(),
    #     )
    #     self.page.wait_for_load_state()
    #     return self
