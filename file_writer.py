import json
import os

import config
import logging
from bs4 import BeautifulSoup


logging.basicConfig(format=config.log_format, filename=config.logger_file,
                    datefmt=config.date_format, filemode="w", level=logging.INFO)
logger = logging.getLogger("FileWriter")


class FileWriter:

    # file_name = config.catalog_file

    def write(self, data, file_name, dir_name=''):
        if dir_name and os.getcwd().split('\\')[-1] != dir_name:
            try:
                os.chdir(dir_name)
            except BaseException as error:
                os.mkdir(dir_name)
                os.chdir(dir_name)
        try:
            with open(file_name, 'w') as json_file:
                json.dump(data, json_file)
            logger.info("Data was successfully recorded")
        except BaseException as error:
            logger.error(f"{file_name}-{error}")
