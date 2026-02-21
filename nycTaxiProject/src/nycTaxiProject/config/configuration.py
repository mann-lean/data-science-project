# Configuration file : We will read the configuration file and create the configuration objects.Configuration file is in yaml format and we will use the yaml library to read the configuration file.
from nycTaxiProject.entity.config_entity import DataIngestionConfig,DataValidationConfig
from nycTaxiProject.util.common import read_yaml,create_directories
from nycTaxiProject.constants import *
import os


class ConfigurationManager:
    def __init__(
            self,
            config_filepath=CONFIG_FILE_PATH,
            params_filepath=PARAMS_FILE_PATH
    ):
        self.config=read_yaml(config_filepath)
        self.params=read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
          config=self.config.data_ingestion
          create_directories([config.root_dir]) # creating the directory for data ingestion
          
          data_ingestion_config=DataIngestionConfig(
                root_dir=config.root_dir,
                source_URL=config.source_URL,
                local_data_file=config.local_data_file,
            #     unzip_dir=config.unzip_dir
          )
          return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config=self.config.data_validation
        create_directories([config.root_dir])

        data_validation_config=DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            data_dir=config.data_dir,
            all_schema=self.schema
        )
        return data_validation_config