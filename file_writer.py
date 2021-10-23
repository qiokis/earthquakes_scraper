import json
import config
import logging


logging.basicConfig(format=config.log_format, filename=config.logger_file,
                    datefmt=config.date_format, filemode="w", level=logging.INFO)
logger = logging.getLogger("FileWriter")


class FileWriter:

    file_name = config.catalog_file

    def write(self, data):
        try:
            with open(self.file_name, 'w') as json_file:
                json.dump(data, json_file)
            logger.info("Data was successfully recorded")
        except BaseException as error:
            logger.error(error)
