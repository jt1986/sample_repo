
import setup_logger
import os
from src.downloader import Downloader
from src.transformation import Transformation
import configparser

if __name__ == "__main__":

    config_file = configparser.ConfigParser()
    config_file.read("config.ini")
    
    if os.getenv('virtual')=="docker":
        file_path=config_file.get('DOCKER', 'FILE_PATH')
        error_file_path=config_file.get('DOCKER', 'ERROR_FILE_PATH')
        output_path=config_file.get('DOCKER', 'OUTPUT_PATH')
        archive_path=config_file.get('DOCKER', 'ARCHIVE_PATH')
    else:
        file_path=config_file.get('LOCAL', 'FILE_PATH')
        error_file_path=config_file.get('LOCAL', 'ERROR_FILE_PATH')
        output_path=config_file.get('LOCAL', 'OUTPUT_PATH')
        archive_path=config_file.get('LOCAL', 'ARCHIVE_PATH')
        
    bucket_name="de-assignment-data-bucket"
    user_project = None
    
    setup_logger.logger.info("Starting to download the data from GCS bucket")
    down = Downloader(bucket_name, file_path, user_project)
    dest_folder = down.download()

    transform_data = Transformation(dest_folder, error_file_path, output_path, archive_path)
    transform_data.transpose()
    setup_logger.logger.info("Successfully transformed data per craft per planet will be found in {} ".format(output_path))
    setup_logger.logger.info("Files which had data error will be found in {} ".format(error_file_path))
    setup_logger.logger.info("Files which had improper naming convention will also be found in {} ".format(error_file_path))
    setup_logger.logger.info("All successfully proccessed files are moved to {} ".format(archive_path))


    
