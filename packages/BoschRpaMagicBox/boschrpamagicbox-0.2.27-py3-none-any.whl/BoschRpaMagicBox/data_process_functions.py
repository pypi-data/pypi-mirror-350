import os
import subprocess
import traceback
from io import StringIO
from time import sleep
from typing import Union

import pandas as pd
import pyperclip

from .helper_functions import create_error_log


def strip_str_column(pd_data: pd.DataFrame, str_column_list: list, upper_column: list = None):
    """This function is used to strip columns in str type

    Args:
        upper_column(list): This is the dict that indicates which column need to be transferred into upper format
        pd_data(pd.DataFrame): This is the instance of pandas DataFrame data
        str_column_list(list):This is the list of column in str type

    Returns:
        pd.DataFrame: pd_data
    """
    if upper_column is None:
        upper_column = []
    if not pd_data.empty:
        for column in str_column_list:
            pd_data[column] = pd_data[column].str.strip()
            if column in upper_column:
                pd_data[column] = pd_data[column].str.upper()
    return pd_data


def load_excel_data(file_path: str, sheet_name: str, upper_column_list: list, header: int = 0, to_dict: bool = False, data_index: str = '',
                    replace_na: bool = False, replace_na_value: str = '', used_cols: list = None, auto_locate_header: bool = False,
                    key_header_column: str = ''):
    """This function is used to transform config data into target format

    Args:
        auto_locate_header(bool): This indicates whether to locate the row index of header row
        key_header_column(str): This is the column which will be used to locate header row
        replace_na(bool): Whether to replace na value with given value
        replace_na_value(str): This is the value to fill na range
        header(int): This is the header number of DataFrame data
        file_path(str): This is the file path of Excel file
        sheet_name(str): This is the name of sheet that contains data
        upper_column_list(list): This is the columns whose values need to be in upper format
        to_dict(bool): This is the flag whether transfer data into dict format
        data_index(str): This is the column that will be index column when data need to be transferred into dict format
        used_cols(list): This is the list of column names which will be used for usecols parameter
    """
    target_data = pd.DataFrame()
    is_loop = True
    while is_loop:
        try:
            if sheet_name:
                target_data = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str, header=header, usecols=used_cols)
            else:
                target_data = pd.read_excel(file_path, dtype=str, header=header, usecols=used_cols)
            is_loop = False
        except ValueError:
            sleep(2)

    if auto_locate_header:
        target_header_index = 0
        for row_index in target_data.index:
            row_data = target_data.loc[row_index]
            if key_header_column in row_data.values:
                target_header_index = row_index + 1
                break

        if sheet_name:
            target_data = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str, header=target_header_index, usecols=used_cols)
        else:
            target_data = pd.read_excel(file_path, dtype=str, header=target_header_index, usecols=used_cols)

    if replace_na:
        target_data.fillna(replace_na_value, inplace=True)

    target_data = strip_str_column(target_data, target_data.columns, upper_column_list)
    if to_dict:
        target_data = target_data[target_data[data_index] != '']
        target_data.set_index(data_index, inplace=True)
        target_data = target_data.to_dict(orient='index')
    return target_data


def load_sap_text_data(file_path: str, dtype: Union[dict, type], key_word: str, remove_unname: bool = True, replace_na: bool = False,
                       replace_na_value: str = '', error_log_folder_path: str = ''):
    """This function is used to load data from txt file

    Args:
        replace_na(bool): This indicates whether to fill NAN value
        replace_na_value(str): This is the value to fill NAN value
        file_path(str): This is the text file path
        dtype(dict | type): This is dtype which will be read as string
        key_word(str): This is the key word to locate column header
        remove_unname(bool): This is the flag whether delete column with 'Unname'
        error_log_folder_path(str): This is the path to record error log

    Returns:
        dict: load_result
    """
    load_result = {'sap_text_data': None, 'has_sap_text_data': False}

    with open(file_path, 'r', encoding='utf-8') as file:
        doc = file.readlines()
        index = 0
        row_length = 0
        text_index = 0
        is_text = False
        for line in doc:
            if key_word in line:
                doc[index] = '\t'.join([i.strip() for i in line.split('\t')])
                row_length = len(doc[index].split('\t'))
                if 'Text' in doc[index].split('\t'):
                    text_index = doc[index].split('\t').index('Text')
                    is_text = True
                if not is_text and 'Document Header Text' in doc[index].split('\t'):
                    text_index = doc[index].split('\t').index('Document Header Text')
                    is_text = True
                break
            index += 1

        if is_text:
            for index, value in enumerate(doc):
                value_list = value.split('\t')
                value_length = len(value_list)
                if value_length > row_length:
                    for j in range(value_length - row_length):
                        value_list[text_index] += value_list[text_index + 1]
                        del value_list[text_index + 1]
                    doc[index] = '\t'.join(value_list)

        doc = '\n'.join(doc)

        for i in range(100):
            try:
                sap_text_data = pd.read_csv(StringIO(doc), dtype=dtype, sep='\t', header=i, quoting=3, low_memory=False)
                sap_text_data_column_list = [str(column).strip() for column in sap_text_data.columns]
                if key_word in sap_text_data_column_list:
                    sap_text_data_column_dict = {column: str(column).strip() for column in sap_text_data.columns}
                    sap_text_data.rename(columns=sap_text_data_column_dict, inplace=True)
                    if remove_unname:
                        sap_text_data_columns = [i for i in sap_text_data.columns if 'Unnamed' not in str(i)]
                        sap_text_data = sap_text_data.loc[:, sap_text_data_columns]
                    if type(dtype) == dict:
                        for column, column_type in dtype.items():
                            if column_type == str:
                                sap_text_data[column] = sap_text_data[column].str.strip()
                    elif dtype == str:
                        for column in sap_text_data.columns:
                            sap_text_data[column] = sap_text_data[column].str.strip()

                    if replace_na:
                        sap_text_data.fillna(replace_na_value, inplace=True)

                    load_result['sap_text_data'] = sap_text_data
                    load_result['has_sap_text_data'] = True
                    break
                else:
                    pass
            except:
                if error_log_folder_path:
                    print(traceback.format_exc())
                    create_error_log(error_log_folder_path, traceback.format_exc())
                pass
    return load_result


def open_sap_with_system_code(system_code: str):
    """This function is used to open sap with system code

    Args:
        system_code(str): POE,PRP ....
    """
    os.system(f'start sapshcut -system={system_code}')


def check_file_download_status(save_folder_path: str, file_name: str):
    """This function is used to check whether file has been downloaded successfully

    Args:
        file_name(str): This is the file name of file that will be saved in save folder
        save_folder_path(str): This is the folder path of save folder
    """
    save_file_path = save_folder_path + os.sep + file_name
    sleep(4)
    is_loop = True
    while is_loop:
        for current_file_name in os.listdir(save_folder_path):
            current_save_file_path = save_folder_path + os.sep + current_file_name
            if os.path.getsize(current_save_file_path) != 0 and file_name.upper().strip() in current_file_name.upper().strip():
                try:
                    os.rename(save_folder_path + os.sep + current_file_name, save_file_path)
                except:
                    pass
                else:
                    is_loop = False
                    break
        sleep(4)


def check_done_indicators_complete(done_file_path: str, key_word: str, wait_time: int = 30):
    """This function is used to check whether all data has been downloaded

    Args:
        done_file_path(str): This is the done file path
        key_word(str): This is the key word to show type
        wait_time(int): This is the wait time duration for checking whether sap data downloaded

    """
    if not os.path.exists(done_file_path):
        print(key_word)
        print(
            f'Wait {wait_time} seconds and will continue to check whether related done file has been downloaded.')
        sleep(wait_time)
        check_done_indicators_complete(done_file_path, key_word, wait_time)
    else:
        return True


def generate_multiple_input_sap_script(multiple_input_list: list, script_header: str = '// Multiple Selection for Company code',
                                       set_value_script: str = '  Set cell[Table,Single value,'):
    """This function is used to generate sap scripts for multiple input of company codes, document number and so on

    Args:
        script_header(str): This is the script header for script function description
        set_value_script(str): This is the set value part sap script
        multiple_input_list(list): This is the list of multiple input values
    """
    start_index = 1
    multiple_input_script_list = [
        f'{script_header}\n', 'Screen SAPLALDB.3000\n']
    for multiple_input in multiple_input_list:
        multiple_input_script_list.append(f'{set_value_script}{start_index}]    	"{multiple_input}"\n')

        if start_index % 7 == 1 and start_index == 8:
            multiple_input_script_list.append('Enter "/82"\n')
            multiple_input_script_list.append(f'{script_header}\n')
            multiple_input_script_list.append('Screen SAPLALDB.3000\n')
            start_index = 1

        start_index += 1
    multiple_input_script_list.append('  Enter "/8"\n')
    return multiple_input_script_list