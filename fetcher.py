import re
import requests as req
from bs4 import BeautifulSoup
import logging
import config

from file_writer import FileWriter

site = "http://www.gsras.ru/ftp/Teleseismic_Catalog/"
max_attempts = 5

logging.basicConfig(format=config.log_format, filename=config.logger_file,
                    datefmt=config.date_format, filemode="w", level=logging.INFO)
logger = logging.getLogger("Fetcher")


YEAR_PATTERN = re.compile(r"\d{4}\.txt")
YEAR_MONTH_PATTERN = re.compile(r"\d{2}m\d{2}\.txt")
YEAR_MONTH_SHARDED_PATTERN = re.compile(r"\d{2}d\d{3}sb\.txt")


class Fetcher:

    fw = FileWriter()
    files = []
    main_catalog = site

    def fetch_link_catalog(self):
        """Function fetches catalogs and files from site with records of earthquakes,
        save it to list and serialize with pickle

        :return:
        """

        res = req.get(self.main_catalog)
        soup = BeautifulSoup(res.text, "lxml")

        for el in soup.find_all("td"):

            file_pattern = re.compile(r"\d{4}\.txt")
            dir_pattern = re.compile(r"^\d{4}/$")

            if dir_pattern.match(el.text):

                temp = self.main_catalog + el.text
                res = req.get(temp)
                soup1 = BeautifulSoup(res.text, "lxml")

                for el1 in soup1.find_all("td"):
                    if any([YEAR_PATTERN.match(el1.text),
                           YEAR_MONTH_PATTERN.match(el1.text),
                           YEAR_MONTH_SHARDED_PATTERN.match(el1.text)]):
                        self.fetch_link_file(el.text + el1.text)

            elif file_pattern.match(el.text):
                self.fetch_link_file(el.text)

        try:
            self.fw.write(self.files)
            logger.info("Catalog was successfully fetched")
        except BaseException as error:
            logger.error(error)

    def fetch_link_file(self, name):
        # Site had changed structure of files for 3 times, so here 3 types of proceeding
        # For files, where file have only year in name
        file_name = name.split('/')[-1]
        if YEAR_PATTERN.match(file_name):
            self.files.append({'link': self.main_catalog + name,
                               'type': 0})
        # For files, where file have year and month in name
        elif YEAR_MONTH_PATTERN.match(file_name):
            self.files.append({'link': self.main_catalog + name,
                               'type': 1})
        # For files, where file have year, month and part of month in name
        elif YEAR_MONTH_SHARDED_PATTERN.match(file_name):
            self.files.append({'link': self.main_catalog + name,
                               'type': 2})

    def fetch_file(self, file_link):
        flag = False
        for i in range(config.max_attempts):
            try:
                logger.info("Attempt:%d | Trying fetch data from %s" % (i, file_link))
                res = req.get(file_link, timeout=2)
                flag = True
            except req.exceptions.Timeout as err:
                logger.error("Failed | %s" % err)
                continue
            break
        if not flag:
            return -1
        logger.info("Fetching successful")
        res = req.get(file_link)
        soup = BeautifulSoup(res.text, "lxml")
        return soup.text