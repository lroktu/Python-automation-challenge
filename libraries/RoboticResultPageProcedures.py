import datetime
import logging
from selenium.webdriver.common.by import By
from libraries.enums.topics import Topics


class RoboticResultPageProcedures:
    """
    Initializes a new instance of the `robotic_result_page_procedures` class.
    Args:
        browser (WebDriver): The Selenium WebDriver instance used to interact with the browser.
        selectors (dict): A dictionary containing CSS selectors used for locating elements on the page.
        input_fields (dict): A dictionary containing input fields and their corresponding values.
    Returns:
        None
    Initializes the following instance variables:
        - browser (WebDriver): The Selenium WebDriver instance used to interact with the browser.
        - selectors (dict): A dictionary containing CSS selectors used for locating elements on the page.
        - input_fields (dict): A dictionary containing input fields and their corresponding values.
        - logger (Logger): The logger instance used for logging messages.
        - popup_clicked (bool): A flag indicating whether the popup has been clicked.
        - days_in_month (int): The number of days in a month.
        - default_wait_time (int): The default wait time for page elements.
    """

    def __init__(self, browser, selectors, input_fields):
        self.browser = browser
        self.selectors = selectors
        self.input_fields = input_fields
        self.logger = logging.getLogger(__name__)
        self.days_in_month = 30
        self.default_wait_time = 25

    def select_checkboxes(self):
        """
        Select checkboxes based on the topics provided in the input fields.
        If the topics include all, no selection is made.
        This function filters results by marking checkboxes, interacts with the browser elements,
        and handles popups if they exist.
        """
        if self.input_fields["topics"] == [Topics.ALL.value]:
            return
        self.logger.debug("Filtering results by marking checkboxes...")
        self.__click_see_all_buttons()
        self.__take_action_if_popup_exists()
        is_see_all_buttons_clicked = True
        for topic in self.input_fields["topics"]:
            self.browser.wait_until_element_is_visible(
                self.selectors["checkbox-menu"], self.default_wait_time
            )
            checkboxes = self.browser.find_elements(
                self.selectors["find-all-checkboxes"]
            )
            for span in checkboxes:
                if is_see_all_buttons_clicked == False:
                    self.logger.debug(span.text)
                    self.__click_see_all_buttons()
                    is_see_all_buttons_clicked = True
                if span.text == topic:
                    checkbox = span.find_element(
                        "xpath", self.selectors["find-specific-checkbox"]
                    )
                    try:
                        checkbox.click()
                        is_see_all_buttons_clicked = False
                        break
                    except Exception as e:
                        self.logger.error(e)
                        self.__take_action_if_popup_exists()
                        checkbox.click()
                        is_see_all_buttons_clicked = False
                        break
                    
    def __click_see_all_buttons(self):
        try:
            self.browser.wait_until_element_is_visible(
                self.selectors["checkbox-menu"], self.default_wait_time
            )
            buttons = self.browser.find_elements(self.selectors["see-all-button"])
            for button in buttons:
                button.click()
        except Exception as e:
            self.logger.error(e)
            self.__take_action_if_popup_exists()
            for button in buttons:
                button.click()

    def select_newest_results(self):
        """
        Selects the newest results by filtering the results page.
        This function filters the results page by selecting the "Newest" option from the dropdown menu.
        It waits until the result page select element is visible and then selects the option with the label "Newest".
        Parameters:
            self (object): The instance of the class.
        Returns:
            None
        """
        self.logger.debug("Filtering results by newest results...")
        self.browser.wait_until_element_is_visible(
            self.selectors["result-page-select-element"], self.default_wait_time
        )
        self.browser.select_from_list_by_label(
            self.selectors["result-page-select-element"],
            self.selectors["select-option-value"],
        )

    def __take_action_if_popup_exists(self):
        """
        Checks if a popup exists on the page and performs an action if it does.
        This function first waits for the popup container to be present on the page.
        It then finds the popup container element and retrieves its shadow root.
        Next, it finds the element with the class name specified in the `popup-dismiss-class-name`
        selector and clicks on it. Finally, it sets the `popup_clicked` flag to True.
        If the popup container is not found, the function logs a warning message.
        Parameters:
            self (object): The instance of the class.
        Returns:
            None
        Raises:
            Exception: If an error occurs while finding or clicking the popup dismiss element.
        """
        try:
            self.browser.wait_until_page_contains_element(
                self.selectors["popup-container-name"], self.default_wait_time
            )
            container_web_element = self.browser.find_element(
                self.selectors["popup-container-name"]
            )
            shadow_root = container_web_element.shadow_root
            shadow_root.find_element(
                By.CLASS_NAME, self.selectors["popup-dismiss-class-name"]
            ).click()

        except Exception as e:
            self.logger.debug("popup doesnt exists")
            self.logger.warning(e)

    def get_search_result_content(self):
        """
        Retrieves the search result content from the webpage.
        This function calculates the minimum timestamp and the current timestamp. It then iterates through the search results
        until it finds results with a timestamp greater than or equal to the minimum timestamp. For each result, it extracts
        the content title, description, timestamp, and image source. The extracted information is stored in a dictionary
        and added to the `results_list`. The function logs the extracted content properties for each result.
        Parameters:
            self (object): The instance of the class.
        Returns:
            list: A list of dictionaries containing the content properties of the search results.
        """
        min_timestamp = self.__calculate_minimum_timestamp()
        content_timestamp = int(datetime.datetime.now().timestamp())
        results_list = []
        while min_timestamp <= content_timestamp:
            self.browser.wait_until_page_contains_element(
                self.selectors["search-result-contents"], self.default_wait_time
            )
            result_ul_element = self.browser.find_element(
                self.selectors["search-result-contents"]
            )
            result_li_elements = result_ul_element.find_elements(By.TAG_NAME, "li")
            if len(result_li_elements) == 0:
                self.logger.debug("No results found")
                break
            for li in result_li_elements:
                content_timestamp = (
                    int(
                        li.find_element(
                            By.CSS_SELECTOR,
                            self.selectors["search-result-timestamp-element"],
                        ).get_attribute("data-timestamp")
                    )
                    // 1000
                )
                if min_timestamp <= content_timestamp:
                    content_properties = {}
                    content_properties["content_title"] = li.find_element(
                        By.CSS_SELECTOR, self.selectors["search-result-title-element"]
                    ).text
                    content_properties["content_description"] = li.find_element(
                        By.CSS_SELECTOR,
                        self.selectors["search-result-description-element"],
                    ).text
                    content_properties["timestamp"] = content_timestamp
                    content_properties["image_src"] = li.find_element(
                        By.CSS_SELECTOR, self.selectors["search-result-image-element"]
                    ).get_attribute("src")
                    results_list.append(content_properties)
                    self.logger.debug(content_properties)
                    continue
                break
            if min_timestamp <= content_timestamp:
                self.browser.click_element_when_clickable(
                    self.selectors["search-result-next-page"]
                )
        return results_list

    def __calculate_minimum_timestamp(self):
        """
        Calculates the minimum timestamp based on the current date, the selected month, and the input fields.

        Returns:
            int: The calculated minimum timestamp.
        """
        days_current_month = datetime.date.today().day
        current_month = 1
        if self.input_fields["till-months-passed"] == current_month:
            days_timedelta = days_current_month
        else:
            days_timedelta = (
                days_current_month
                + (self.input_fields["till-months-passed"] - 1) * self.days_in_month
            )
        min_timestamp = int(
            (
                datetime.datetime.now() - datetime.timedelta(days=days_timedelta)
            ).timestamp()
        )
        return min_timestamp
