import os
import pandas


default_directory = "earthquake_data"


def create_excel(output_file_name, sheet_name, data_directory=default_directory, file_name=''):
    """
    Function creating excel file and place there info from json file or
     info from whole directory with json files
    :param output_file_name: Name of excel file
    :param sheet_name: Name of excel sheet
    :param data_directory: Name of directory with json files
    :param file_name: Name of exact json file (optional)
    :return:
    """
    directory = data_directory
    if file_name:
        data = pandas.DataFrame(pandas.read_json(f"{directory}\\{file_name}"))
    else:
        first = f"{directory}\\{os.listdir(directory)[0]}"
        data = pandas.DataFrame(pandas.read_json(first))
        for file in os.listdir(directory)[1:]:
            next = pandas.DataFrame(pandas.read_json(f"{directory}\\{file}"))
            data = data.append(next)
    data.to_excel(output_file_name+'.xlsx', sheet_name=sheet_name)


if __name__ == "__main__":
    create_excel(input("Enter name of excel file: "),
                 input("Enter name of excel sheet: "),
                 input("Enter name of directory with data: "),
                 input("Enter name of file with data (optional): "))