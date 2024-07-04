
from RPA.Browser.Selenium import Selenium
import json

class custom_browser_config:
    def __init__(self):
        options = {
            "timeout": 120,
            "implicit_wait": 30,
            "page_load_timeout": 60,
            "auto_close": False
        }

        with open('config/page.json') as f:
            data = json.load(f)
        self.browser = Selenium(**options)
        self.browser.set_selenium_speed(1.0)
        self.browser.open_available_browser(headless=True, url=data["url"], maximized=True)

    def get_browser(self):
        return self.browser
    def close(self):
        self.browser.close_browser()