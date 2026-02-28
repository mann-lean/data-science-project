import os
from pathlib import Path
import pandas as pd
from nycTaxiProject.entity.config_entity import DataValidationConfig
from nycTaxiProject.util.common import read_yaml,create_directories

class Data_Validation:
    def __init__(self,config:DataValidationConfig):
        self.config=config
    
    def validation_all_columns(self)->bool:
        try:
            validation_status=None
            df=pd.read_csv("artifacts/data_ingestion/data.csv")
            col=list(df.columns)

            all_schema=self.config.all_schema.keys()

            for col in all_schema:
                if col not in all_schema:
                    validation_status=False
                    with open(self.config.STATUS_FILE,'w') as f:
                        f.write(f"Validation Status : {validation_status}")
                    break
                else:
                    validation_status=True
                    with open(self.config.STATUS_FILE,'w') as f:
                        f.write(f"Validation Status : {validation_status}")

            return validation_status
        except Exception as e:
            raise e