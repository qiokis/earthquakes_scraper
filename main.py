import logging

import config as c
from fetcher import Fetcher
from file_parser import Parser


logging.basicConfig(format=c.log_format, filename=c.logger_file,
                    datefmt=c.date_format, filemode="w", level=logging.INFO)
logger = logging.getLogger("Main")


def initial_message():
    print("Welcome to the earthquake scraping script.")
    print(f"Data of earthquakes will be scraped from {c.site}.")
    print("-"*100)


if __name__ == '__main__':
    initial_message()
    Fetcher().fetch_link_catalog()
    Parser().parse()
    logger.info("Done")


