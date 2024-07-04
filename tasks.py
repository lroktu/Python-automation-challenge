import json
import logging
from robocorp.tasks import task
from RPA.Robocorp.WorkItems import WorkItems
from selenium.webdriver.common.keys import Keys
from libraries.CustomBrowserConfig import CustomBrowserConfig as custom_browser
from libraries.dataStorageProcedures import DataStorageProcedures
from libraries.RoboticResultPageProcedures import (
    RoboticResultPageProcedures as rtc_respag_procedures,
)
from libraries.data_analysis import data_analysis
from libraries.schema_validator import schema_validator


@task
def minimal_task():
    """
    Executes a minimal task that opens a browser, navigates to a result page, extracts data,
    performs data analysis, and stores the results. The task is retried up to 5 times if an
    error occurs during data extraction. If the task is successful, the data is analyzed and
    stored in an output folder.
    Parameters:
    None
    Returns:
    None
    Raises:
    Exception: If an error occurs during the execution of the task.
    """
    try:
        input_fields = get_work_items()
        selectors = read_selectors()
        is_data_extracted = False
        number_of_attempts = 0
        while not is_data_extracted:
            try:
                if number_of_attempts < 5:
                    logging.info("Opening browser...")
                    browser = custom_browser().get_browser()
                    logging.info("Transitioning to result page...")
                    goto_result_page(browser, selectors, input_fields)
                    logging.info("Extracting data...")
                    captured_data = execute_result_page_procedures(
                        rtc_respag_procedures(browser, selectors, input_fields)
                    )
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
        logging.info(
            "Results were successfully generated and stored in the output folder."
        )
    except Exception as e:
        logging.error(e)



def execute_result_page_procedures(result_page_procedures):
    """
    Executes the result page procedures.
    Args:
        result_page_procedures (object): An instance of the result page procedures class.
    Returns:
        list: A list of search result content.
    Raises:
        None
    """
    result_page_procedures.select_newest_results()
    result_page_procedures.select_checkboxes()
    return result_page_procedures.get_search_result_content()


def goto_result_page(browser, selectors, input_fields):
    """
    Navigates to the result page by interacting with the browser.

    Args:
        browser: The browser object used for navigation.
        selectors: Dictionary containing web element selectors.
        input_fields: Dictionary containing input fields data.

    Returns:
        None
    """
    browser.wait_until_element_is_visible(selectors["search-button"])
    browser.click_button(selectors["search-button"])
    browser.input_text_when_element_is_visible(
        selectors["search-form"], input_fields["search-phrase"] + Keys.ENTER
    )


def execute_data_analysis(captured_data, search_phrase):
    """
    Executes data analysis on the captured data.
    Args:
        captured_data (list): A list of dictionaries representing the captured data.
        search_phrase (str): The search phrase to analyze.
    Returns:
        None
    Raises:
        None
    """
    d_analysis = data_analysis()
    for item in captured_data:
        text = item["content_title"] + item["content_description"]
        item["search_phrase_ocurrences"] = d_analysis.count_number_of_ocurrences(
            text, search_phrase
        )
        item["fiat_currency_exists"] = d_analysis.is_dolar_fiat_currency_present(text)


def execute_storage_procedures(captured_data):
    """
    Executes storage procedures on the captured data by saving the results using the data storage procedures class.

    Args:
        captured_data (list): A list of dictionaries representing the captured data to be saved.

    Returns:
        None
    """
    DataStorageProcedures().save_data_results(captured_data)


def get_work_items():
    """
    Retrieves work items from the `WorkItems` class, validates the input fields using the `schema_validator` class,
    and returns the validated input fields.
    Returns:
        dict: A dictionary containing the validated input fields.
    Raises:
        jsonschema.ValidationError: If the input fields fail validation against the schema.
    """
    input_items = WorkItems()
    input_items.get_input_work_item()
    input_fields = input_items.get_work_item_variables()
    return schema_validator().validate(input_fields)


def read_selectors():
    """
    Reads selectors from the 'config/locators.json' file and returns them as a dictionary.
    Returns:
        dict: A dictionary containing the selectors loaded from the 'config/locators.json' file.
    """
    with open("config/locators.json", encoding="utf-8") as f:
        selectors = json.load(f)
    return selectors
