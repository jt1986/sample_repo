import pytest
from src.file_handler import FileHandler
import configparser

def test_check_file_name():
    config = configparser.ConfigParser()
    config.read("config.ini")
    pattern = "([^\a_z_]+)_([^\a_z_]+)_([0-9]+)_([0-9]+).csv"
    file_path=config.get('TEST', 'FILE_PATH')
    error_path=config.get('TEST', 'ERROR_FILE_PATH')
    list_files = ['lander_saturn_20210301_013306.csv', 'lander_venus_20210301_003124.csv', 'rocket_saturn_20210301_121033.csv', 'rocket_venus_20210308_035720.csv', 'notright_format.csv']
    result = FileHandler.check_file_name(pattern, file_path, error_path)
    files_expected = 'notright_format.csv'
    assert files_expected == result


    