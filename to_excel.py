import os

def create_excel(output_file_name, sheet_name):
    directory = "earthquake_data/"
    first = directory + os.listdir(directory)[0]
    data = pandas.DataFrame(pandas.read_json(first))
    for file in os.listdir(directory)[1:]:
        next = pandas.DataFrame(pandas.read_json(directory+file))
        data = data.append(next)
    data.to_excel(output_file_name, sheet_name=sheet_name)


if __name__ == "__main__":
    create_excel()
