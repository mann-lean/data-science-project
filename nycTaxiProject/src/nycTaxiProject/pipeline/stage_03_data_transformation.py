from nycTaxiProject.components.data_transformation import Data_Transformation
from nycTaxiProject.config.configuration import ConfigurationManager
from nycTaxiProject import logger
from pathlib import Path
STAGE_NAME="DATA TRANSFORMATION STAGE"

class DataTransformationPipeline:
    def __init__(self):
        pass
    def main(self):
        try:
            status_file_path=Path("artifacts/data_validation/status.txt")
            if not status_file_path.exists():
                raise Exception("Validation Status.txt file isn't found!! Did Stage 2 run??")
            with open(status_file_path,'r')as f:
                status_content=f.read()
            if "True" not in status_content:
                raise Exception("Data Validation (False) is Failed! Halting the pipeline to prevent Data Transformation on bad data.")
            
            logger.info("Data Validation Passed! Proceeding with Data Transformation..")

            config=ConfigurationManager()
            data_transform=Data_Transformation(config.get_data_transformation_config())
            data_transform.data_transforamtion()

        except Exception as e:
            logger.exception(e)
            raise e

if __name__=="__main__":
    try:
        logger.info(">>>>>>>STAGE: DATA TRANSFORMATION STARTED<<<<<<<<< ")
        # config=ConfigurationManager()
        # data_transformed_config=config.get_data_transformation_config()
        # data_transform=Data_Transformation(config=data_transformed_config) #class obj
        # data_transform.data_transforamtion()
        obj=DataTransformationPipeline()
        obj.main()
        logger.info(">>>>>>>STAGE: DATA TRANSFORMATION ENDED<<<<<<<<< ")

    except Exception as e:
        logger.exception(e)
        raise e