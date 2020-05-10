import re

def format_control(string, control_list):
    string = re.sub(control_list[0], control_list[1], str(string))
    return string

def number_text_split(string):
    number = re.findall(r'[0-9]',string)
    return number[0]

def type_transfer(input_data, type_):
    try:
        return type_(input_data)
    except:
        raise ValueError("can't transfer unless you match the data type")