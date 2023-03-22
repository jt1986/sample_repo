import setup_logger
import re
import pandas as pd
from src.file_handler import FileHandler
class Transformation:
    _time_pattern = "([0-9]+)_([0-9]+)"
    _file_name_pattern = "([^\a_z_]+)_([^\a_z_]+)"
    _pattern = "([^\a_z_]+)_([^\a_z_]+)_([0-9]+)_([0-9]+).csv"
    _datetime_file_format = "%Y%m%d_%H%M%S"


    def __init__(self, file_path, error_file_path, output_path, archive_path):
        self._file_path = file_path
        self._error_file_path = error_file_path
        self._output_path = output_path
        self._archive_path = archive_path
    
    def transpose(self):
        """
        This function does the following
        If the file paths does not exist it would create them based on the configuration 
        Data is read from the files and transposed 
        split_id - function would extract the mid value of UUID
        transform_size - would convert the size from an integer into a `magnitude`
        After successful transformation it would move to respective folders
        1. Success to output folder path
        2. Failure to error folder path
        3. Archive to archive folder path. Archive would show you what was processed before. This also allows you to reprocess them again
        """
        FileHandler.dir_creator(self._archive_path)
        FileHandler.dir_creator(self._output_path)
        FileHandler.dir_creator(self._error_file_path)
        
        FileHandler.check_file_name(self._pattern, self._file_path,  self._error_file_path)

        setup_logger.logger.info("Transforming the data has begun")
        files = FileHandler.list_files(self._file_path)
        files.sort()

        for file in files:
            unique_id = []
            magnitude = []           
            date_time_match = re.search(self._time_pattern, file)
            if date_time_match is None:
                setup_logger.logger.warn("file format of not specificed pattern {}".format(file))
                exit()
            
            file_name_match = re.search(self._file_name_pattern, file)
            if file_name_match is None:
                setup_logger.logger.warn("file format of not specificed pattern {}".format(file))
                exit()
            
            file_name = file_name_match[0]
            
            # extracting timestamp from the file name
            datetime_str = date_time_match[0]
            timestamp_obj=pd.to_datetime(datetime_str, format=self._datetime_file_format)
            
            data_obj = pd.read_csv(self._file_path+'/'+file, delimiter=',')
            
            # lower casing all column names
            data_obj.columns = data_obj.columns.str.lower()
            # timestamp column
            data_obj['timestamp'] = timestamp_obj
            
            # validate size is all integers. 
            # This will help create an identifier for those which are not integers. They will be represented as True
            data_obj['size_isdigit']= pd.to_numeric(data_obj['size'].fillna('0'), errors='coerce').isna() 
            
            # extract error data on size column
            error_size_data = data_obj[data_obj['size_isdigit']==True]
            
            #cleaning the actual object
            data_obj = data_obj.drop(data_obj[data_obj['size_isdigit']==True].index)
            data_obj = data_obj.drop(data_obj[data_obj['size'].isna()].index)
            data_obj['size'] = pd.to_numeric(data_obj['size'])

            # extract middle value of UUID
            data_obj['id_split']=data_obj['id'].str.split('-')
            col_index = list(data_obj.columns).index('id_split')
            for value in data_obj.keys():
                if value == 'id_split':
                    unique_id = self.split_id(value, data_obj, unique_id)
                if value == 'size':
                    magnitude = self.transform_size(value, data_obj, magnitude)

            data_obj['unique_id'] = unique_id
            data_obj['magnitude'] = magnitude

            data_obj = data_obj.drop(columns=['size', 'id_split', 'id', 'size_isdigit'])
            data_obj = data_obj.reset_index(drop=True)

            FileHandler.save_to_csv(self._output_path+file_name, ",", data_obj)
            FileHandler.save_to_csv(self._error_file_path+"/error_data", ",", error_size_data)
            
            FileHandler.move_files(self._file_path+"/"+file, self._archive_path)
            del data_obj
            del error_size_data
        setup_logger.logger.info("Completed transforming the data")

    def split_id(self, value, data_obj, unique_id):
        id_data = data_obj[value]
        for val in id_data:
            middle = float(len(val))/2
            if middle % 2 != 0:
                unique_id.append(val[int(middle - 0.5)])
            else:
                unique_id.append(val[int(middle)])
        return unique_id

    def transform_size(self, value, data_obj, magnitude):
        size_data = data_obj[value]
        for val in size_data:
            if 500 <= val < 1000:
                magnitude.append('massive')
            elif 100 <= val < 500:
                magnitude.append('big')
            elif 50 <= val < 100:
                magnitude.append('medium')
            elif 10 <= val <50:
                magnitude.append('small')
            else:
                magnitude.append('tiny')
        return magnitude