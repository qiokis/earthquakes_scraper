import json
import os
import pickle
import logging
import sys

from bs4 import BeautifulSoup
import requests as req
import re


logging.basicConfig(filename="log.log", filemode="w", level=logging.INFO)
logger = logging.getLogger("logger")
default_dir = 'earthquake_data'

def fetch_files():
    """Function fetches catalogs and files from site with records of earthquakes,
    save it to list and serialize with pickle

    :return:
    """
    main_catalog = "http://www.gsras.ru/ftp/Teleseismic_Catalog/"
    files = []
    res = req.get(main_catalog)
    soup = BeautifulSoup(res.text, "lxml")
    for el in soup.find_all("td"):
        if re.match(r"^(\d{4}/|\d{4}\.txt)$", el.text):
            if not re.match(r".*\.txt", el.text):
                temp = main_catalog + el.text
                res = req.get(temp)
                soup1 = BeautifulSoup(res.text, "lxml")
                for el1 in soup1.find_all("td"):
                    if re.match(r"^(\d+[a-zA-Z]\d+[a-zA-Z]*)", el1.text):
                        files.append(main_catalog + el.text + el1.text)
            else:
                files.append(main_catalog + el.text)

    with open("files.pickle", "wb") as f:
        pickle.dump(files, f)


def get_files():
    """Function return files from dump

    :return: list of files
    """
    with open("files.pickle", "rb") as f:
        return pickle.load(f)


def parse_files(dir_name=default_dir):
    """Function parsing data from files and save it to json

    :return:
    """
    logger.info("Parsing started")

    try:
        logger.info(f"Creating \"{dir_name}\" directory")
        os.mkdir(dir_name)
        logger.info(f"\"{dir_name}\" directory created")
    except FileExistsError as err:
        logger.warning(f"\"{dir_name}\" directory is exists")

    logger.info(f"Data directory = {dir_name}")
    files = get_files()
    file_name = 0
    for file in files:
        datas = []
        data = dict()
        flag = False
        for i in range(5):
            try:
                logger.info("Attempt:%d | Trying fetch data from %s" % (i, file))
                res = req.get(file, timeout=2)
                flag = True
            except req.exceptions.Timeout as err:
                logger.error("Failed | %s" % err)
                continue
            break
        if not flag:
            continue
        logger.info("Fetching successful")
        all_data = res.text.split("------------------------------------------------------------")[2].split("\n")
        for el in all_data:
            string = el.strip()
            if re.match(r"^\d+\s+\d+", string):
                elements = string.split()
                if len(elements) == 9:
                    data.update({"id": elements[0]})
                    data.update({"day": elements[1]})
                    data.update({"time": elements[2]})
                    data.update({"latitude": "%s %s" % (elements[3], elements[4])})
                    data.update({"longitude": "%s %s" % (elements[5], elements[6])})
                    data.update({"magnitude": elements[8]})
                    datas.append(data.copy())
                    data.clear()
        datas = datas
        info = dict()
        info.update({"URL": file})
        with open(f"{dir_name}/" + str(file_name) + ".json", "w") as f:
            json.dump(info, f)
            # json.dump(datas, f)
        logger.info(f"{dir_name}/%d.json was created" % file_name)
        file_name += 1
    logger.info("Done")


if __name__ == '__main__':
    if len(temp := sys.argv) > 1:
        parse_files(temp[1])
    else:
        parse_files()
