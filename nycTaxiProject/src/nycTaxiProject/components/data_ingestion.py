import os
import kagglehub
from pathlib import Path
from nycTaxiProject.util.common import read_yaml,create_directories,get_size
from nycTaxiProject.entity.config_entity import DataIngestionConfig
from nycTaxiProject import logger

class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config=config

    def download_file(self)->str:   # download the file from the URL to local directory
        """Fetch data from the URL to local directory"""
        try:
            dataset_url=self.config.source_URL
            download_path=self.config.local_data_file
            parent_dir=os.path.dirname(download_path) # why we are using parent dir because we want to create the directory if it does not exist before downloading the file
            os.makedirs(parent_dir,exist_ok=True)
            logger.info(f"downloading the file form{dataset_url} into file {download_path}")

            kagglehub.dataset_download(handle=dataset_url,output_dir=download_path,force_download=True)
            # filename,headers=request.urlretrieve(url=dataset_url,filename=download_path)

            logger.info(f"File downloaded successfully & saved @ {download_path} with size {get_size(Path(download_path))}")

        except Exception as e:
            raise e