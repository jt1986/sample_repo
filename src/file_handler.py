import os
import re
import shutil
import setup_logger
import pandas as pd

class FileHandler:


    @staticmethod
    def dir_creator(file_path):
        isExists = os.path.exists(file_path)
        if not isExists:
            os.makedirs(file_path)
    
    @staticmethod
    def move_files(current_location, file_move_location):
        shutil.move(current_location, file_move_location)
    
    @staticmethod
    def list_files(file_path):
        return os.listdir(file_path)

    def pandas_file_reader():
        return None
    
    def save_to_csv(file_path, seperator, data):
        extension = ".csv"
        data.to_csv(file_path+extension, sep=seperator, index=False, mode='a')



    def check_file_name(pattern, file_path, error_file_path):
        """
        This function will only check for file name pattern. 
        If it is not a valid file name pattern file will be moved to an error file path
        """
        setup_logger.logger.info("validating file name pattern")
        files = FileHandler.list_files(file_path)
        error_file = []
        
        for file in files:
            match = re.search(pattern, file)
            if match is None:
                current_file_path = file_path+'/'+file
                error_path = error_file_path+'/'+file
                setup_logger.logger.info("file is not a match {}. moving to location {}".format(file, error_file_path))
                FileHandler.dir_creator(error_file_path)
                FileHandler.move_files(current_file_path, error_path)
                return file

                
