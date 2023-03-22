from google.cloud import storage
import setup_logger
import os
from src.file_handler import FileHandler
class Downloader:

    def __init__(self, bucket_name, file_location, user_project):
        self._bucket_name = bucket_name
        self._file_location = file_location
        self._user_project = user_project
        

    def storage_connection(self, bucket_name, user_project):
        client = storage.Client.create_anonymous_client()
        bucket = client.bucket(self._bucket_name, user_project=self._user_project)
        return client, bucket

    def blob_listing(self, client, bucket):
        blobs = client.list_blobs(bucket)
        return blobs

    def download(self):
        """
        This function will only download the files from the GCS bucket and load it into a local folder.
        Since this is a test project I didn't want to alter the location of the actual files.
        Args:
            bucket_name (str): GCS location where the data is currently stored
            user_project (str): project name here will be set to None as this is an anonymous client connection
            file_location (str): local folder location where the file is going to be downloaded from GCS bucket
        """

        file_incr = 0
        files_downloaded = 0

        client, bucket = self.storage_connection(self._bucket_name, self._user_project)
        blobs = self.blob_listing(client, bucket)

        for blob_file_count in blobs:
            file_incr +=1

        setup_logger.logger.info("Total number of files to read: {}".format(file_incr))

        blobs = self.blob_listing(client, bucket)
        setup_logger.logger.info('Reading through the GCS bucket, starting to download...')
        for blob in blobs:
            destination_uri ='{}/{}'.format(self._file_location, blob.name)
            destination_folder_name = blob.name.split('/')[0]
            destination_folder = '{}/{}'.format(self._file_location, destination_folder_name)

            FileHandler.dir_creator(destination_folder)

            blob.download_to_filename(filename=destination_uri, client=client)
            files_downloaded += 1
        if files_downloaded==file_incr:
            setup_logger.logger.info('Downloaded {} files to: {}'.format(files_downloaded,destination_folder))
        else:
            setup_logger.logger.info('Could not download {} file/files'.format(file_incr-files_downloaded)) 
        return destination_folder