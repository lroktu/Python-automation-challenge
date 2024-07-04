

import datetime
from libraries.enums.topics import Topics
import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
class robotic_result_page_procedures:

    def __init__(self, browser, selectors, input_fields):
        self.browser = browser
        self.selectors = selectors
        self.input_fields = input_fields
        self.logger = logging.getLogger(__name__)
        self.popup_clicked = False
        self.days_in_month = 30
        self.default_wait_time = 10

    def select_checkboxes(self):
        if (self.input_fields["topics"] == [Topics.ALL.value]):
            return
        self.logger.info("Filtering results by marking checkboxes...")
        self.__click_see_all_buttons()
        self.__take_action_if_popup_exists()
        is_see_all_buttons_clicked = True
        for topic in self.input_fields["topics"]:
            self.browser.wait_until_element_is_visible(self.selectors["checkbox-menu"], self.default_wait_time)
            checkboxes = self.browser.find_elements(self.selectors["find-all-checkboxes"])
            for span in checkboxes:
                if (self.popup_clicked == False):
                    self.__take_action_if_popup_exists()     
                if is_see_all_buttons_clicked == False:
                        self.logger.info(span.text)
                        self.__click_see_all_buttons()
                        is_see_all_buttons_clicked = True
                if (span.text == topic):    
                    checkbox = span.find_element("xpath", self.selectors["find-specific-checkbox"])
                    checkbox.click()
                    is_see_all_buttons_clicked = False
                    break

    def __click_see_all_buttons(self):
        self.browser.wait_until_element_is_visible(self.selectors["checkbox-menu"], self.default_wait_time)
        buttons = self.browser.find_elements(self.selectors["see-all-button"])
        for button in buttons:
            button.click()

    def select_newest_results(self):
        self.logger.info("Filtering results by newest results...")
        self.browser.wait_until_element_is_visible(self.selectors["result-page-select-element"], self.default_wait_time)
        self.browser.select_from_list_by_label(self.selectors["result-page-select-element"], self.selectors["select-option-value"])
    
    def __take_action_if_popup_exists(self):
        try:
            self.browser.wait_until_page_contains_element(self.selectors["popup-container-name"], self.default_wait_time)
            container_web_element = self.browser.find_element(self.selectors["popup-container-name"])
            shadow_root = container_web_element.shadow_root
            shadow_root.find_element(By.CLASS_NAME, self.selectors["popup-dismiss-class-name"]).click()
            self.popup_clicked = True

        except Exception as e:
            self.logger.info("popup doesnt exists")
            self.logger.warning(e)
    
    def get_search_result_content(self):
        min_timestamp = self.__calculate_minimum_timestamp()
        content_timestamp = int(datetime.datetime.now().timestamp())
        results_list = []
        while (min_timestamp <= content_timestamp):
            self.browser.wait_until_page_contains_element(self.selectors["search-result-contents"], self.default_wait_time)
            result_ul_element = self.browser.find_element(self.selectors["search-result-contents"])
            result_li_elements = result_ul_element.find_elements(By.TAG_NAME, "li")
            if (len(result_li_elements) == 0):
                self.logger.info("No results found")
                break
            for li in result_li_elements:
                content_timestamp = int(li.find_element(By.CSS_SELECTOR, self.selectors["search-result-timestamp-element"]).get_attribute("data-timestamp")) // 1000
                if min_timestamp <= content_timestamp:
                    content_properties = {}
                    content_properties["content_title"] = li.find_element(By.CSS_SELECTOR, self.selectors["search-result-title-element"]).text
                    content_properties["content_description"] = li.find_element(By.CSS_SELECTOR, self.selectors["search-result-description-element"]).text
                    content_properties["timestamp"] = content_timestamp
                    content_properties["image_src"] = li.find_element(By.CSS_SELECTOR, self.selectors["search-result-image-element"]).get_attribute("src")
                    results_list.append(content_properties)
                    self.logger.info(content_properties)
                    continue
                break
            if (min_timestamp <= content_timestamp):
                self.browser.click_element_when_clickable(self.selectors["search-result-next-page"])
        return results_list
    
    def __calculate_minimum_timestamp(self):
        days_current_month = datetime.date.today().day
        current_month = 1
        if (self.input_fields["till-months-passed"] == current_month):
            days_timedelta = days_current_month
        else:
            days_timedelta = days_current_month + (self.input_fields["till-months-passed"] - 1) * self.days_in_month
        min_timestamp = int((datetime.datetime.now() - datetime.timedelta(days=days_timedelta)).timestamp())
        return min_timestamp