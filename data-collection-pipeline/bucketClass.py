import requests # used to download files
import boto3 # used to access AWS resources
import dataClass # used to access common variables
import os # used to join directory paths

class bucket:
    '''
    This class contains all the functions that interact with the S3 bucket. 

    This class will upload files to and download files from the bucket and display the bucket contents

    Attributes:

    Functions:
        __bucketUploadImage(self, path, imageFileName)
            Uploads an image to the bucket
        
        __bucketUploadJson(self, path, jsonFileName)
            Uploads a json to the bucket

        __bucketDownloadJson(self, url, jsonFileName)
            Downloads a json to the local directory

        __bucketDownloadImage(self, url, imageFileName)
            Downloads an image to the local directory

        __bucketDisplay(self)
            Displays the bucket contents
    '''

    data = dataClass.data()

    def __bucketUploadImage(self, path, imageFileName) -> None:
        '''
        This function uploads the image to the bucket
        
        Args:
             path(str): The directory the image is stored in
             imageFileName(str): The string used to name the image 
        
        Returns:
        
        '''

        s3_client = boto3.client('s3')
        response = s3_client.upload_file(path, data.bucketName, imageFileName) # (file_name, bucket, object_name)
    
    def __bucketUploadJson(self, path, jsonFileName) -> None:
        '''
        This function uploads the json to the bucket
        
        Args:
             path(str): The directory the json is stored
             jsonFileName(str): The string used to name the file 
        
        Returns:
        
        '''

        s3_client = boto3.client('s3')
        response = s3_client.upload_file(path, data.bucketName, jsonFileName) # (file_name, bucket, object_name)

    def __bucketDownloadJson(self, url, jsonFileName) -> None:
        '''
        This function downloads the json into the local directory
        
        Args:
             url(str): The url for the file stored in the bucket
             jsonFileName(str): The string used to name the file 
        
        Returns:
        
        '''

        response = requests.get(url, jsonFileName)
        path = os.path.join(data.dataDirectory, jsonFileName)
        with open(path, 'wb') as f:
            f.write(response.content)

    def __bucketDownloadImage(self, url, imageFileName) -> None:

        '''
        This function downloads the image into the local directory
        
        Args:
             url(str): The url for the file stored in the bucket
             jsonFileName(str): The string used to name the file 
        
        Returns:
        
        '''

        response = requests.get(url, imageFileName)
        path = os.path.join(data.dataDirectory, imageFileName)
        with open(path, 'wb') as f:
            f.write(response.content)

    def __bucketDisplay(self) -> None:
        '''
        This function displays which files in the bucket
        
        Args:
        
        Returns:
        
        '''

        s3 = boto3.resource('s3')
        my_bucket = s3.Bucket(data.bucketName)
        for file in my_bucket.objects.all():
            print(file.key)

bucket()