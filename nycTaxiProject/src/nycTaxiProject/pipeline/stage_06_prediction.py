import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import OneHotEncoder, StandardScaler,TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from nycTaxiProject import logger
from pathlib import Path

class Inference_transform:
    def __init__(self, preprocessor_path="artifacts/data_transformation/train/preprocessor.pkl"):
        # Load the preprocessor once when the object is created
        self.preprocessor = joblib.load(preprocessor_path)

    def dateTime_extraction(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Extracting Date & time features """
        df['pickupDateTime'] = pd.to_datetime(df['pickupDateTime'], format='ISO8601')
        df['dropoffDateTime'] = pd.to_datetime(df['dropoffDateTime'], format='ISO8601')

        df['pickup_dow'] = df['pickupDateTime'].dt.dayofweek

        df['is_weekend'] = df['pickup_dow'].isin([5, 6]).astype(int)

        df['pickup_hr'] = df['pickupDateTime'].dt.hour

        df['pickup_ampm'] = (df['pickup_hr'] >= 12).astype(int)

        df['trip_duration_mins'] = (df['dropoffDateTime'] - df['pickupDateTime']).dt.total_seconds() / 60
    
        df = df.drop(columns=['pickupDateTime','dropoffDateTime'])
        return df
    
    def feature_extraction(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Business logic feature engineering """
        df['farePerMile'] = df['fare_amount'] / df['trip_distance']
        
        # Safely handle division by zero if duration is exactly 0
        df['avg_speed'] = df['trip_distance'] / (df['trip_duration_mins'] / 60).replace(0, 0.001)
        
        df['pre_tip_amount'] = (
            df['fare_amount'] + df['extra'] + df['mta_tax'] + 
            df['tolls_amount'] + df['improvement_surcharge'] + 
            df['congestion_surcharge'] + df['airport_fee'] 
        )
        
        df = df.drop(columns=['mta_tax','improvement_surcharge'])
        
        aritport_zones = [1, 132, 138, 139] 
        df['Is_Airport_Trip'] = (
            df['pulocationid'].isin(aritport_zones) | df['dolocationid'].isin(aritport_zones)
        ).astype(int)
        
        df['is_airport_peak_hour'] = df['pickup_hr'].apply(lambda hr: 1 if 4 <= hr <= 6 else 0)
        df['is_pm_peak_hour'] = df['pickup_hr'].apply(lambda hr: 1 if 16 <= hr <= 18 else 0) 
        
        df['PickUpHr_sin'] = np.sin(2 * np.pi * df['pickup_hr'] / 24.0)
        df['PickUpHr_cos'] = np.cos(2 * np.pi * df['pickup_hr'] / 24.0)
        
        df = df.drop(columns=['pickup_hr'])
        return df

    def encode_feature(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Apply the loaded preprocessor """
        # Only transform the data!
        encode_array = self.preprocessor.transform(df)
        names = self.preprocessor.get_feature_names_out()
        encoded_df = pd.DataFrame(encode_array, columns=names)

        # Passthrough columns
        additional_cols = ['is_weekend', 'pickup_ampm', 'Is_Airport_Trip', 'is_airport_peak_hour', 'is_pm_peak_hour', 'PickUpHr_sin', 'PickUpHr_cos']
        transformed_df = pd.concat([encoded_df, df[additional_cols].reset_index(drop=True)], axis=1)

        return transformed_df
    # final calling method for input data transformation 
    def process(self, input_dict: dict) -> pd.DataFrame:
        """ The master function to orchestrate the pipeline """
        df = pd.DataFrame(input_dict)
        df = self.dateTime_extraction(df)
        df = self.feature_extraction(df)
        final_df = self.encode_feature(df)
        return final_df
    
class PredictionPipeline:
        def __init__(self):
            self.model_path=Path("artifacts/model_training/sgdModel.pkl")
            self.model=joblib.load(self.model_path)
            self.Inference_transform=Inference_transform()

        def predict(self,user_input : dict):
            try:
                model_input=self.Inference_transform.process(user_input)
                prediction=self.model.predict(model_input)
                return prediction

            except Exception as e:
                logger.exception(e)
                raise e