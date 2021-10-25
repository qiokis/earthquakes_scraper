import logging
import json
import re

import config as c
from file_writer import FileWriter
from fetcher import Fetcher

# logging.basicConfig(format=c.log_format, filename=c.logger_file,
#                     datefmt=c.date_format, filemode="w", level=logging.INFO)
logger = logging.getLogger("Parser")


class Parser:

    months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
              'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10,
              'November': 11, 'December': 12}
    dir_name = c.json_directory
    links = list()
    fw = FileWriter()

    def __init__(self):
        with open(c.catalog_file, 'r') as file:
            self.links = json.load(file)

    def parse(self):
        """Function parsing data from files and save it to json

        :return:
        """

        for dictionary in self.links:
            file_link, file_type = dictionary['link'], dictionary['type']

            all_data = Fetcher.fetch_file(file_link)

            logger.info(f"{file_link} parsing started")

            if file_type == 0:
                result = self.parse_year_file(all_data)
                year = re.search(r'\d+', file_link.split('/')[-1])
                file_name = year.group() + '.json'
            elif file_type == 1:
                year, month = re.findall(r'\d+', file_link.split('/')[-1])
                month = str(int(month))
                if int(str(year)[0]) >= 3:
                    year = f"19{year}"
                else:
                    year = f"20{year}"
                result = self.parse_year_month_file(all_data, {'year': year, 'month': month})
                file_name = f"{year}-{month}.json"
            else:
                link = file_link.split('/')[-1]
                year = str(int(re.search(r'\d{2}d', link).group()[:-1]))
                month = str(int(re.search(r'd\d{2}', link).group()[1:]))
                part = str(int(re.search(r'\dsb', link).group()[:-2]))
                if int(year) >= 30:
                    year = f"19{year}"
                else:
                    if len(year) < 2:
                        year = f"200{year}"
                    else:
                        year = f"20{year}"

                result = self.parse_year_month_sharded_file(all_data,
                                                    {'year': year, 'month': month, 'part': part})
                file_name = f"{year}-{month}-{part}.json"

            logger.info(f"{file_link} parsed successfully")
            self.fw.write(result, file_name, c.json_directory)

    def parse_year_file(self, site_data):
        date = {'time': 0, 'day': 0, 'month': 0, 'year': 0}
        datas = []
        data = dict()
        for el in site_data:
            string = el.strip()
            if re.match(r"\w+\s\d{4}", string):
                month, year = string.split(' ')
                date['year'], date['month'] = year, self.months[month]
            if re.match(r"^\d+\s+\d+", string):
                elements = string.split()
                if len(elements) == 9:
                    date['day'] = int(elements[1])
                    if date['day'] == 0:
                        print(string)
                    conc_date = f"{date['year']}-{date['month']}-{date['day']}T{elements[2]}"
                    data.update({'date': conc_date})
                    data.update({"latitude": "%s %s" % (elements[3], elements[4])})
                    data.update({"longitude": "%s %s" % (elements[5], elements[6])})
                    data.update({"magnitude": elements[8]})
                    datas.append(data.copy())
                    data.clear()
        return datas

    def parse_year_month_file(self, site_data, inp_date):
        date = {'time': 0, 'day': 0}
        date.update(inp_date)
        datas = []
        data = dict()
        for el in site_data:
            string = el.strip()
            if re.match(r"^\d+\s+\d+", string):
                elements = string.split()
                if len(elements) == 9:
                    date['day'] = int(elements[1])
                    if date['day'] == 0:
                        print(string)
                    conc_date = f"{date['year']}-{date['month']}-{date['day']}T{elements[2]}"
                    data.update({'date': conc_date})
                    data.update({"latitude": "%s %s" % (elements[3], elements[4])})
                    data.update({"longitude": "%s %s" % (elements[5], elements[6])})
                    data.update({"magnitude": elements[8]})
                    datas.append(data.copy())
                    data.clear()
        return datas

    def parse_year_month_sharded_file(self, site_data, inp_date):
        date = {'time': 0, 'day': 0}
        date.update(inp_date)
        datas = []
        data = dict()
        for el in site_data:
            string = el.strip()
            if re.match(r"^\d+\s+\d+", string):
                elements = string.split()
                if len(elements) == 9:
                    date['day'] = int(elements[1])
                    if date['day'] == 0:
                        print(string)
                    conc_date = f"{date['year']}-{date['month']}-{date['day']}T{elements[2]}"
                    data.update({'date': conc_date})
                    data.update({"latitude": "%s %s" % (elements[3], elements[4])})
                    data.update({"longitude": "%s %s" % (elements[5], elements[6])})
                    data.update({"magnitude": elements[8]})
                    datas.append(data.copy())
                    data.clear()
        return datas
