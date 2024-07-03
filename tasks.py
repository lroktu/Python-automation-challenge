import json
import time
from robocorp.tasks import task
from RPA.Robocorp.WorkItems import WorkItems
import logging
from libraries.custom_browser_config import custom_browser_config as custom_browser
from libraries.robotic_result_page_procedures import robotic_result_page_procedures as rtc_respag_procedures
from libraries.schema_validator import schema_validator
from selenium.webdriver.common.keys import Keys

@task
def minimal_task():
    browser = custom_browser().get_browser()
    try:
        input_fields = get_work_items()
        selectors = read_selectors()
        goto_result_page(browser, selectors, input_fields)
        execute_result_page_procedures(rtc_respag_procedures(browser, selectors, input_fields))
        time.sleep(60)
        browser.close_browser()
    except Exception as e:
        logging.error(e)
        time.sleep(30)
        browser.close_browser()

def execute_result_page_procedures(result_page_procedures):
    result_page_procedures.select_newest_results()
    result_page_procedures.select_checkboxes()
    result_page_procedures.get_search_result_content()

def goto_result_page(browser, selectors, input_fields):
    browser.wait_until_element_is_visible(selectors["search-button"])
    browser.click_button(selectors["search-button"])
    browser.input_text_when_element_is_visible(selectors["search-form"], input_fields["search-phrase"] +Keys.ENTER)
    browser.wait_and_click_button(selectors["search-submit-button"])


def get_work_items():
    input_items = WorkItems()
    input_items.get_input_work_item()
    input_fields = input_items.get_work_item_variables()
    return schema_validator().validate(input_fields)

def read_selectors():
    with open('config/locators.json') as f:
            selectors = json.load(f)
    return selectors
