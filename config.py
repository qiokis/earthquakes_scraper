import re

site = "http://www.gsras.ru/ftp/Teleseismic_Catalog/"
max_attempts = 5

logger_file = "log.log"
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
date_format = "%d-%m-%Y %I:%M:%S"

catalog_file = "catalog.json"
json_directory = "earthquake_data"

YEAR_PATTERN = re.compile(r"\d{4}(.txt)?")
YEAR_MONTH_PATTERN = re.compile(r"\d{2}m\d{2}(.txt)?")
YEAR_MONTH_SHARDED_PATTERN = re.compile(r"\d{2}d\d{3}sb(.txt)?")