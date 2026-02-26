from nycTaxiProject.util.common import read_yaml,create_directories, save_evaluation
from nycTaxiProject.config.configuration import ConfigurationManager
from nycTaxiProject.entity.config_entity import ModelEvaluationConfig
from nycTaxiProject import logger
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from sklearn.linear_model import SGDRegressor
import numpy as np
import joblib
import pandas as pd
import mlflow
import dagshub
from pathlib import Path

class Model_Evaluation:
    def __init__(self,config=ModelEvaluationConfig):
        self.config=config
        self.model=joblib.load(self.config.model_dir) #importing model(.pkl )
    def evaluate_model(self, x_train,y_train,x_test, y_test): #why argument  need model,when we are loading the model from the directory? because we are loading the model from the directory, we don't need to pass the model as an argument to the evaluate_model method. We can remove the model argument from the method definition and directly load the model within the method using joblib.load(self.config.model_dir). Here's how you can modify the evaluate_model method:
        try:
            #1 Initializing Dagshub logger
            dagshub.init(repo_owner='mann-lean', repo_name='data-science-project', mlflow=True) # Initialize the DagsHub logger with the repository owner, repository name, and enable MLflow logging
            #2 set the tracking URI for MLflow
            mlflow.set_tracking_uri(self.config.mlflow_uri) # Set the tracking URI for MLflow to the DagsHub MLflow server
            model=self.model
           
            with mlflow.start_run(): # Start an MLflow run to log parameters, metrics, and artifacts
                # Prediciton for both training and testing data
                y_train_pred = model.predict(x_train) #training data prediction
                y_test_pred = model.predict(x_test) #testing data prediction

                # TRAINING DATA EVALUATION METRICS
                train_r2 = round(r2_score(y_train, y_train_pred),4)
                train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred)).round(4)
                train_mse=round(mean_squared_error(y_train, y_train_pred),4)
                train_mae = round(mean_absolute_error(y_train, y_train_pred),4)

                # TESTING DATA EVALUATION METRICS
                test_r2 = round(r2_score(y_test, y_test_pred),4)
                test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred)).round(4)
                test_mse=round(mean_squared_error(y_test, y_test_pred),4)
                test_mae = round(mean_absolute_error(y_test, y_test_pred),4)
                
                print(f"-----------Training Evaluation-------------")
                print(f"R2 Score:   {train_r2:.4f}")
                print(f"RMSE:       {train_rmse:.4f}")
                print(f"MSE:        {train_mse:.4f}")
                print(f"MAE:        {train_mae:.4f}")

                print(f"-----------Testing Evaluation-------------")
                print(f"R2 Score:   {test_r2:.4f}")
                print(f"RMSE:       {test_rmse:.4f}")
                print(f"MSE:        {test_mse:.4f}")
                print(f"MAE:        {test_mae:.4f}")

                # saving evaluation metrics in a dictionary
                evalutaion_dict={
                                 "training_R2_Score":train_r2,
                                 "training_RMSE":train_rmse,
                                 "training_MSE":train_mse,
                                 "training_MAE":train_mae,
                                 "testing_R2_Score":test_r2,
                                 "testing_RMSE":test_rmse,
                                 "testing_MSE":test_mse,
                                 "testing_MAE":test_mae
                                 }
                # saving evaluation metrics in a JSON file (LOCALLY)
                save_evaluation(evalutaion_dict,Path(self.config.model_evaluation))
                
            # 4. LOG PARAMS: Save hyperparameter configurations (e.g., alpha, penalty)
                if self.config.all_params:
                    mlflow.log_params(self.config.all_params)
            # 5. LOG METRICS: Log evaluation metrics (e.g., R2, RMSE, MSE, MAE)
                mlflow.log_metric(f"training_R2_Score", train_r2)
                mlflow.log_metric(f"training_RMSE", train_rmse)
                mlflow.log_metric(f"training_MSE", train_mse)
                mlflow.log_metric(f"training_MAE", train_mae)
                
                mlflow.log_metric(f"testing_R2_Score", test_r2)
                mlflow.log_metric(f"testing_RMSE", test_rmse)
                mlflow.log_metric(f"testing_MSE", test_mse)
                mlflow.log_metric(f"testing_MAE", test_mae)
            # 6. LOG MODEL: Optionally, log the trained model itself for future reference
                mlflow.sklearn.log_model(model, "model", registered_model_name="SGDRegressor")
                
        except Exception as e:
            logger.exception(e)
            raise e
