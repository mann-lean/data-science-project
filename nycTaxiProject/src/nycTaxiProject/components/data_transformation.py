import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder, TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from nycTaxiProject import logger
from nycTaxiProject.config.configuration import DataTransformationConfig

class Data_Transformation:
    def __init__(self,config=DataTransformationConfig):
        self.config=config
    # if we assigned in a config argument constructor,& then do we have to pass the config argument while creating the object of this class? No, because we have already assigned a default value to the config argument in the constructor, which is DataTransformationConfig. This means that if we create an object of the Data_Transformation class without passing any arguments, it will use the default value of DataTransformationConfig for the config parameter. However, if we want to use a different configuration, we can pass it as an argument when creating the object.
    def data_transforamtion(self): # do we have to pass config argument here? No, because we have already assigned a default value to the config argument in the constructor, which is DataTransformationConfig. This means that if we call the data_transforamtion method without passing any arguments, it will use the default value of DataTransformationConfig for the config parameter. However, if we want to use a different configuration, we can pass it as an argument when calling the method.
        try:
            data_dir=self.config.data_dir
#  LOAD DATA
            def load_data(df):
                df=pd.read_csv(data_dir)
                df.columns=df.columns.str.lower() # converting all columns to lower case
                logger.info(f"Data Loaded from {data_dir} successfully")
                return df

# FILLING MISSING VALUE
            def filling_missing(df):
                df['passenger_count']=df['passenger_count'].fillna(1)  #after finding mean of this columns we got 1.37 value ,after rounding we're assuming it as 1
                df['congestion_surcharge']=df['congestion_surcharge'].fillna(0)
                df['airport_fee']=df['airport_fee'].fillna(0)
                df['ratecodeid']=df['ratecodeid'].fillna(99) #after investigating thsi column ,we replacing with 9.9(Null/unknown)
                df=df.drop(columns='store_and_fwd_flag') #we're droppoing this columns ,(N:99%+) value.so i could not impact on out predictive model
                logger.info(f"FILLING MISSING VALUES")
                return df

# PREPROCESSING DATE & TIME
            def preprocessingDateTime(df):
                # 1. Convert to datetime using the correct format for your data
                # Using format='ISO8601' handles the "2023-01-01T00:32:10" format automatically
                df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'], format='ISO8601')
                df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'], format='ISO8601')

                # 2. Extract Month and Day of Week
                df['pickup_month'] = df['tpep_pickup_datetime'].dt.month
                df['dropoff_month'] = df['tpep_dropoff_datetime'].dt.month

                df['pickup_dow'] = df['tpep_pickup_datetime'].dt.dayofweek
                df['dropoff_dow'] = df['tpep_dropoff_datetime'].dt.dayofweek

                # 3. Weekend Flag (1 for Sat/Sun, 0 otherwise)
                df['is_weekend'] = df['pickup_dow'].isin([5, 6]).astype(int)

                # 4. Extract Hour (Faster to get as int directly)
                df['pickup_hr'] = df['tpep_pickup_datetime'].dt.hour
                df['dropoff_hr'] = df['tpep_dropoff_datetime'].dt.hour

                # 5. AM/PM Indicator (PM = 1, AM = 0)
                # We can do this based on the hour (>= 12) which is much faster than string parsing
                df['pickup_ampm'] = (df['pickup_hr'] >= 12).astype(int)
                df['dropoff_ampm'] = (df['dropoff_hr'] >= 12).astype(int)

                # 6. Trip duration in minutes
                df['trip_duration_mins'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60

                # 7. Filtering minutes
                df=df[(df['trip_duration_mins']>0) & (df['trip_duration_mins']<120)]

                logger.info(f"Preprocessing DateTime completed")
                return df

# DATA CLEANING 
            def data_cleaning(df):
                df=df.drop(columns=['tpep_pickup_datetime','tpep_dropoff_datetime'])
                df[(df['trip_distance']>0.1) & (df['trip_distance']<100)]# because there is no less than 0 trip distance &no such max miles,we simply gave it max 100
                df=df[~df.select_dtypes(include="number").lt(0).any(axis=1)] #it will remove those values  which is less than 0, .lt(0):means less than 0 vlaues

                df=df[df["total_amount"]>3.7]
                df=df[df["total_amount"]<1000]

                df=df[df['payment_type']==1]

                df=df.drop(columns=['total_amount','payment_type','dropoff_month','dropoff_dow','dropoff_ampm','dropoff_hr'])

                # removing 99 cause invalid code
                df=df[df['ratecodeid']<99]
                df=df[df['fare_amount']>=3]
                df=df[df['trip_distance']>0.01]

                df=df[df['passenger_count']>0]
                df=df[df['passenger_count']<=6]

                df=df.drop(columns=['pickup_month'])

                df=df[df['tip_amount']>0]
                df=df[df['fare_amount'] < 200]

                logger.info(f"Data Cleaning completed")
                return df

# FEATURE ENGINEERING
            def feature_engineering(df):
                # adding pre tip amount
                df['pre_tip_amount'] = (
                    df['fare_amount'] + 
                    df['extra'] + 
                    df['mta_tax'] + 
                    df['tolls_amount'] + 
                    df['improvement_surcharge'] + 
                    df['congestion_surcharge'] + 
                    df['airport_fee']
                )
                df=df.drop(columns=['mta_tax','improvement_surcharge']) # dropping these columns as they are not useful for model
                # adding new Flag column based on airport zones  
                aritport_zones=[1,132,138,139] #airport zones
                df['Is_Airport_Trip']=(
                    df['pulocationid'].isin(aritport_zones) | df['dolocationid'].isin(aritport_zones)
                ).astype(int)
                # Flag airport peak hour
                # peak window(4AM-6AM)
                df['is_airport_peak_hour']=df['pickup_hr'].apply(
                    lambda hr:1 if 4<=hr<=6 else 0
                )
                # evening peak hour
                df['is_pm_peak_hour']=df['pickup_hr'].apply(
                    lambda hr:1 if 16<=hr<=18 else 0) 
                # calculating avg speed of trip     [avg_speed = trip_distance / trip_duration_mins]
                df['avg_speed']=df['trip_distance']/df['trip_duration_mins']
                df=df[df['avg_speed'] < 60]
                
                # Fare per mile
                df['farePerMile']=df['fare_amount']/df['trip_distance']
                df=df[df['farePerMile'] < 50]

                # pickup hr to cynical feature
                # 1. Create Sine and Cosine features
                df['PickUpHr_sin'] = np.sin(2 * np.pi * df['pickup_hr'] / 24.0)
                df['PickUpHr_cos'] = np.cos(2 * np.pi * df['pickup_hr'] / 24.0)
                # 2. Drop the original linear hour column
                df.drop(columns=['pickup_hr'], inplace=True)
                # df=df[df['ratecodeid']==1] # we are only taking ratecodeid 1 because it is the most common rate code and it will help us to reduce the noise in our data(Consistent data)
                
                logger.info(f"Feature Engineering completed")
                return df
    
    # TRAIN - TEST SPLIT 20%
            def train_test_split(df) -> pd.DataFrame:
                test_size=int(len(df)*0.2)
                # shuffling our data
                df=df.sample(frac=1,random_state=432).reset_index(drop=True)

                # selecting trining & target columns
                target=df['tip_amount']
                features=df.drop(columns=['tip_amount'])

                # reserve all but the last 1000000 rows for training - anything else for testing
                x_train,x_test=features.iloc[:-test_size],features.iloc[-test_size:]
                y_train,y_test=target.iloc[:-test_size],target.iloc[-test_size:]

                logger.info(f"Train-Test Split completed with test size: {test_size}")
                return x_train,x_test,y_train,y_test
    
    # CLIPPING OUTLIERS on INDEPENDENT VARIABLE   (x_train,x_test)
            def clipping_independent(x_train,x_test)->pd.DataFrame:
                # clipping on 99.5th percentile to remove extreme outliers
                fare_cap = x_train['fare_amount'].quantile(0.995)
                dist_cap = x_train['trip_distance'].quantile(0.995)
                # clip the values in the columns to the respective caps
                x_train['fare_amount']=x_train['fare_amount'].clip(upper=fare_cap)
                x_train['trip_distance']=x_train['trip_distance'].clip(upper=dist_cap)

                x_test['fare_amount']=x_test['fare_amount'].clip(upper=fare_cap)
                x_test['trip_distance']=x_test['trip_distance'].clip(upper=dist_cap)

                logger.info(f"Clipping Outliers completed")
                return x_train,x_test

    # ENCODDING Independent variable
            def encoding_independent(x_train,x_test,y_train):
                # 1. Define Features (Same as before)
                cat_onehot_features = ['vendorid','ratecodeid', 'pickup_dow']
                cat_target_features = ['pulocationid', 'dolocationid']
                numerical_features = [
                    'passenger_count', 'extra', 'tolls_amount', 
                    'congestion_surcharge', 'airport_fee', 
                    'trip_distance', 'fare_amount', 'farePerMile',
                     'pre_tip_amount','avg_speed','trip_duration_mins'
                ]

                #2. Column Transformer
                preprocessor=ColumnTransformer(
                    transformers=[
                        ('onehot',OneHotEncoder(handle_unknown='ignore', drop='first', sparse_output=False),cat_onehot_features),
                        ('target',TargetEncoder(smooth="auto", target_type='continuous'),cat_target_features),
                        ('standardScaler',StandardScaler(),numerical_features)
                    ]
                )
                # preprocessor.set_output(transform="pandas") # magic line for turning into dataframe
                # fit & transform the training data
                x_trainEncoded=preprocessor.fit_transform(x_train,y_train)

                # fit & transform the training data
                x_testEncoded=preprocessor.transform(x_test)

                # After fit_transform
                names = preprocessor.get_feature_names_out()
                encoded_train = pd.DataFrame(x_trainEncoded, columns=names, index=x_train.index)
                encoded_test = pd.DataFrame(x_testEncoded, columns=names, index=x_test.index)

                # combining some columns which were not transformed by column transformer
                # non_transformed_cols = [col for col in x_train.columns if col not in names]
                # encoded_train = pd.concat([encoded_train, x_train[non_transformed_cols]], axis=1)
                # encoded_test = pd.concat([encoded_test, x_test[non_transformed_cols]], axis=1)

                addidtional_cols=['is_weekend', 'pickup_ampm','Is_Airport_Trip', 'is_airport_peak_hour', 'is_pm_peak_hour','PickUpHr_sin', 'PickUpHr_cos']
                encoded_train = pd.concat([encoded_train, x_train[addidtional_cols]], axis=1)
                encoded_test = pd.concat([encoded_test, x_test[addidtional_cols]], axis=1)

                return encoded_train,encoded_test
            
    #SAVING BEFORE ENCODING DATA
            def save_before_encoding(x_train,x_test):
                train_before_dir=self.config.train_before
                test_before_dir=self.config.test_before

                x_train.to_csv(train_before_dir,index=False)
                x_test.to_csv(test_before_dir,index=False)

                logger.info(f"Before Encoding data saved at {self.config.before_encoding} successfully...")

    # SAVING Complete TRANSFORMED DATA
            def save_transformed_data(x_train,x_test,y_train,y_test):
                transformed_data_dir=self.config.root_dir
                x_train_dir=self.config.x_train_dir
                y_train_dir=self.config.y_train_dir
                x_test_dir=self.config.x_test_dir
                y_test_dir=self.config.y_test_dir

                x_train.to_csv(x_train_dir,index=False)
                y_train.to_csv(y_train_dir,index=False)
                x_test.to_csv(x_test_dir,index=False)
                y_test.to_csv(y_test_dir,index=False)

                logger.info(f"Trasnfomred data saved at {transformed_data_dir} successfully...")
                
                 


    # calling all FUNCTIONS
            df=load_data(data_dir) #loading data
            df=filling_missing(df) #filling missing value
            df=preprocessingDateTime(df)  # preprocessing data & time
            df=data_cleaning(df)# data cleaning
            df=feature_engineering(df) #feature Engineering
            x_train,x_test,y_train,y_test=train_test_split(df) # train test split
            x_train,x_test=clipping_independent(x_train,x_test) # cipping outliers on x variavles
            save_before_encoding(x_train,x_test) # saving before encoding data
            x_train,x_test=encoding_independent(x_train,x_test,y_train) #encoding train-test spit
            save_transformed_data(x_train,x_test,y_train,y_test) # saving transformed data
    
            


        except Exception as e:
            logger.error(f"Error in data transformation: {e}")
            raise e