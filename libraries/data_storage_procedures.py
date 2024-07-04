from concurrent.futures import ThreadPoolExecutor
import json
import os
from RPA.HTTP import HTTP
from RPA.Excel.Files import Files
from robocorp.tasks import get_output_dir
import logging
import datetime
class data_storage_procedures:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.excel_config = self.__read_excel_config()

    def save_data_results(self, data_results):
        """
        Saves the data results by downloading and modifying data using the given data results.
        Parameters:
            data_results (list): A list of dictionaries containing the data to be saved.
        Returns:
            None
        """
        try:
            modified_data = self.__download_executor(data_results)
            self.__create_and_save_workbook(modified_data)
        except Exception as e:
            self.logger.error(str(e))

    def __create_and_save_workbook(self, data_results):
        """
        Creates a new Excel workbook and saves it to the output directory with the given data results.
        Parameters:
            data_results (list): A list of dictionaries containing the data to be saved in the workbook.
        Returns:
            None
        """
        self.logger.info("Creating and saving data on xlxs file workbook...")
        if ((data_results == None) | len(data_results) == 0):
            self.logger.info("No data to save")
            return

        excel = Files()
        excel.create_workbook(path=os.path.join(get_output_dir(),self.excel_config["workbook_name"]), sheet_name=self.excel_config["worksheet_name"])
        excel.append_rows_to_worksheet(data_results, header=True, name=self.excel_config["worksheet_name"])
        excel.save_workbook()

    def __download_executor(self, data_results):
        self.logger.info("Downloading images...")
        with ThreadPoolExecutor(max_workers=self.excel_config["number_of_thread_workers"]) as executor: 
            results = executor.map(self.__download_and_save_image, data_results)
        return list(results)
    
    def __download_and_save_image(self, data):
        """
        Downloads an image from the given URL and saves it locally.
        Parameters:
            url (str): The URL of the image to download.
        Returns:
            None
        """
        try:
            base_path = os.path.basename(data["image_src"])
            picture_filename = f"picture-{base_path}"
            data["picture_filename"] = picture_filename
            data["timestamp"] = datetime.datetime.fromtimestamp(data["timestamp"]).strftime("%m/%d/%y")
            http = HTTP()
            http.download(data["image_src"], os.path.join(get_output_dir(), picture_filename))
            self.logger.info(f"Downloaded image from URL: {data['image_src']}")
            del data['image_src']
        except Exception as e:
            msg = f"Error downloading image from URL: {data['url']}"
            self.logger.error(str(e))
            data["error"] = msg

        return data

    def __read_excel_config(self):
        """
        Reads the configuration for an Excel file from the 'config/excel.json' file.
        Returns:
            dict: The configuration for the Excel file.
        """
        with open('config/excel.json') as f:
            excel_config = json.load(f)
        return excel_config