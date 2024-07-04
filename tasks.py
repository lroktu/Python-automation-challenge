import json
from robocorp.tasks import task
from RPA.Robocorp.WorkItems import WorkItems
import logging
from libraries.custom_browser_config import custom_browser_config as custom_browser
from libraries.data_storage_procedures import data_storage_procedures
from libraries.robotic_result_page_procedures import robotic_result_page_procedures as rtc_respag_procedures
from libraries.data_analysis import data_analysis
from libraries.schema_validator import schema_validator
from selenium.webdriver.common.keys import Keys

@task
def minimal_task():
    try:
        input_fields = get_work_items()
        selectors = read_selectors()
        is_data_extracted = False
        number_of_attempts = 0
        while (is_data_extracted == False):
            try:
                if (number_of_attempts < 5):
                    logging.info("Opening browser...")
                    browser = custom_browser().get_browser()
                    logging.info("Transitioning to result page...")
                    goto_result_page(browser, selectors, input_fields)
                    logging.info("Extracting data...")
                    captured_data = execute_result_page_procedures(rtc_respag_procedures(browser, selectors, input_fields))
                    is_data_extracted = True
                    browser.close_browser()
            except Exception as e:
                logging.error(str(e))
                logging.error("Error extracting data, trying again...")
                browser.close_browser()
                number_of_attempts += 1
        logging.info("Data extracted successfully. Now executing data analysis...")
        execute_data_analysis(captured_data, input_fields["search-phrase"])
        logging.info("Data analysis completed. Now executing storage procedures...")
        execute_storage_procedures(captured_data)
        logging.info("Results were successfully generated and stored in the output folder.")
    except Exception as e:
        logging.error(e)
        browser.close_browser()

def execute_result_page_procedures(result_page_procedures):
    result_page_procedures.select_newest_results()
    result_page_procedures.select_checkboxes()
    return result_page_procedures.get_search_result_content()

def goto_result_page(browser, selectors, input_fields):
    browser.wait_until_element_is_visible(selectors["search-button"])
    browser.click_button(selectors["search-button"])
    browser.input_text_when_element_is_visible(selectors["search-form"], input_fields["search-phrase"] +Keys.ENTER)

def execute_data_analysis(captured_data, search_phrase):
    d_analysis = data_analysis()
    for item in captured_data:
        text = item["content_title"] + item["content_description"]
        item["search_phrase_ocurrences"] = d_analysis.count_number_of_ocurrences(text, search_phrase)
        item["fiat_currency_exists"] = d_analysis.is_dolar_fiat_currency_present(text)

def execute_storage_procedures(captured_data):
    data_storage_procedures().save_data_results(captured_data)
    
def get_work_items():
    input_items = WorkItems()
    input_items.get_input_work_item()
    input_fields = input_items.get_work_item_variables()
    return schema_validator().validate(input_fields)

def read_selectors():
    with open('config/locators.json') as f:
            selectors = json.load(f)
    return selectors
