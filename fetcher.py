import re
import requests as req
from bs4 import BeautifulSoup
import logging
import config as c

from file_writer import FileWriter

site = "http://www.gsras.ru/ftp/Teleseismic_Catalog/"
max_attempts = 5

logging.basicConfig(format=c.log_format, filename=c.logger_file,
                    datefmt=c.date_format, filemode="w", level=logging.INFO)
logger = logging.getLogger("Fetcher")


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

        logger.info(f"Fetching from {c.site} started")

        for el in soup.find_all("td"):

            file_pattern = re.compile(r"\d{4}\.txt")
            dir_pattern = re.compile(r"^\d{4}/$")

            if dir_pattern.match(el.text):

                temp = self.main_catalog + el.text
                res = req.get(temp)
                soup1 = BeautifulSoup(res.text, "lxml")
                print(el)

                for el1 in soup1.find_all("td"):
                    if any([c.YEAR_PATTERN.match(el1.text),
                           c.YEAR_MONTH_PATTERN.match(el1.text),
                           c.YEAR_MONTH_SHARDED_PATTERN.match(el1.text)]):
                        self.fetch_link_file(el.text + el1.text)

            elif file_pattern.match(el.text):
                self.fetch_link_file(el.text)

        try:
            self.fw.write(self.files, c.catalog_file)
            logger.info("Catalog was successfully fetched")
        except BaseException as error:
            logger.error(error)

    def fetch_link_file(self, name):
        # Site had changed structure of files for 3 times, so here 3 types of proceeding
        # For files, where file have only year in name
        file_name = name.split('/')[-1]
        file_type = -1
        if c.YEAR_PATTERN.match(file_name):
            file_type = 0
        # For files, where file have year and month in name
        elif c.YEAR_MONTH_PATTERN.match(file_name):
            file_type = 1
        # For files, where file have year, month and part of month in name
        elif c.YEAR_MONTH_SHARDED_PATTERN.match(file_name):
            file_type = 2
        self.files.append({'link': self.main_catalog + name,
                           'type': file_type})

    @staticmethod
    def fetch_file(file_link):
        flag = False
        res = None
        for i in range(c.max_attempts):
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
        soup = BeautifulSoup(res.text, "lxml")
        return soup.text