# Configuration file : We will read the configuration file and create the configuration objects.Configuration file is in yaml format and we will use the yaml library to read the configuration file.
from nycTaxiProject.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainingConfig,ModelEvaluationConfig
from nycTaxiProject.util.common import read_yaml,create_directories,save_evaluation
from nycTaxiProject.constants import *
import os


class ConfigurationManager:
    def __init__(
            self,
            config_filepath=CONFIG_FILE_PATH,
            params_filepath=PARAMS_FILE_PATH,
            schema_filepath=SCHEMA_FILE_PATH
    ):
        self.config=read_yaml(config_filepath)
        self.params=read_yaml(params_filepath)
        self.schema=read_yaml(schema_filepath)

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
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
         config=self.config.data_transformation
         create_directories([config.root_dir])

         data_transformed_config=DataTransformationConfig(
              root_dir=config.root_dir,
              data_dir=config.data_dir,
              transformed_data=config.transformed_data
         )
         return data_transformed_config

    def get_data_transformation_config(self) -> DataTransformationConfig:
         config=self.config.data_transformation
         create_directories([config.root_dir])
         create_directories([config.train])
         create_directories([config.test])
         create_directories([config.before_encoding])

         data_transformed_config=DataTransformationConfig(
              root_dir=config.root_dir,
              data_dir=config.data_dir,
              train=config.train,
              test=config.test,
              x_train_dir=config.x_train_dir,
              y_train_dir=config.y_train_dir,
              x_test_dir=config.x_test_dir,
              y_test_dir=config.y_test_dir,
              before_encoding=config.before_encoding,
              train_before=config.train_before,
              test_before=config.test_before,
              preprocessor_file=config.preprocessor_file
         )
         return data_transformed_config
    
    def get_model_training_config(self)->ModelTrainingConfig:
        config=self.config.model_training
        params=self.params
        create_directories([config.root_dir])

        model_training_config=ModelTrainingConfig(
            root_dir=config.root_dir,
            xtraining_data=config.xtraining_data,
            ytraining_data=config.ytraining_data,
            model_dir=config.model_dir,
            loss=params.loss,
            penalty=params.penalty,
            alpha=params.alpha,
            max_iter=params.max_iter,
            tol=params.tol,
            random_state=params.random_state,
            learning_rate=params.learning_rate,
            eta0=params.eta0

        )
        return model_training_config
    
    def get_model_evaluation(self)->ModelEvaluationConfig:
        config=self.config.model_evaluation
        create_directories([config.root_dir])

        model_evaluation_config=ModelEvaluationConfig(
            root_dir=config.root_dir,
            x_train_dir=config.x_train_dir,
            y_train_dir=config.y_train_dir,
            x_test_dir=config.x_test_dir,
            y_test_dir=config.y_test_dir,
            model_dir=config.model_dir,
            all_params= self.params,
            mlflow_uri= "https://dagshub.com/mann-lean/data-science-project.mlflow",
            model_evaluation=config.model_evaluation
        )
        return model_evaluation_config