from nycTaxiProject.config.configuration import ConfigurationManager
from nycTaxiProject.util.common import read_yaml,create_directories,save_model
from nycTaxiProject.entity.config_entity import ModelTrainingConfig
from nycTaxiProject import logger 
from sklearn.linear_model import SGDRegressor
import pandas as pd
from pathlib import Path

class Model_Trainer:
    def __init__(self,config=ModelTrainingConfig):
        self.config=config

    def train_model(self):
        try:
            x_train=pd.read_csv(self.config.xtraining_data) #fetching DataFrame from the csv file which is stored in the path mentioned in the config file.
            y_train=pd.read_csv(self.config.ytraining_data) #fetching DataFrame from the csv file which is stored in the path mentioned in the config file.
            model_dir=Path(self.config.model_dir)
            param_kwargs=dict(
                loss=self.config.loss,
                penalty=self.config.penalty,
                alpha=self.config.alpha,
                max_iter=self.config.max_iter,
                tol=self.config.tol,
                random_state=self.config.random_state,
                learning_rate=self.config.learning_rate,
                eta0=self.config.eta0
            )


            def sgd_model(param_kwargs,x_train,y_train):
                model=SGDRegressor(**param_kwargs)
                model.fit(x_train,y_train.values.ravel())
                return model
            
            @staticmethod # Static method is a method that belongs to a class rather than an instance of the class. It can be called on the class itself, rather than on an instance of the class. Static methods do not have access to the instance (self) or class (cls) variables, and they are defined using the @staticmethod decorator.
            def save_trained_model(model,model_dir:Path):
                save_model(model=model,path=model_dir)

            model=sgd_model(param_kwargs,x_train,y_train)
            save_trained_model(model=model,model_dir=model_dir)

        except Exception as e:
            logger.exception(e)
            raise e