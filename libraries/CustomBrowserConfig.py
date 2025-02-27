import json
from RPA.Browser.Selenium import Selenium


class CustomBrowserConfig:
    """
    Initializes the CustomBrowserConfig object with specified options and opens a browser based on the configuration in 'config/page.json'.
    """

    def __init__(self):
        options = {
            "timeout": 120,
            "implicit_wait": 30,
            "page_load_timeout": 60,
            "auto_close": False,
        }

        with open("config/page.json", encoding="utf-8") as f:
            data = json.load(f)
        self.browser = Selenium(**options)
        self.browser.set_selenium_speed(1.0)
        self.browser.open_available_browser(
            headless=True, url=data["url"], maximized=True
        )

    def get_browser(self):
        """
        Returns the browser object.
        :return: The browser object.
        :rtype: Selenium
        """
        return self.browser

    def close(self):
        """
        Closes the browser.
        """
        self.browser.close_browser()
