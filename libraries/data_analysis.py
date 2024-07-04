
import logging
import re

class data_analysis:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.fiat_patterns = [ r"\$\d+(?:\.\d+)?",  r"\d+ dollars", r"\d+ USD"]
    
    def count_number_of_ocurrences(self, text, search_phrase):
        self.logger.info("Counting number of search phrase ocurrences")
        text_lower = text.lower()
        return text_lower.count(search_phrase)

    def is_dolar_fiat_currency_present(self, text):
        self.logger.info("Checking if fiat currency is present on text")
        for pattern in self.fiat_patterns:
            if re.search(pattern, text):
                return True
        return False
