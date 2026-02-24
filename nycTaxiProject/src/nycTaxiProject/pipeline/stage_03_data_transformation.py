from nycTaxiProject.components.data_transformation import Data_Transformation
from nycTaxiProject.config.configuration import ConfigurationManager
from nycTaxiProject import logger

STAGE_NAME="DATA TRANSFORMATION STAGE"

class DataTransformationPipeline:
    def __init__(self):
        pass
    def main(self):
        config=ConfigurationManager()
        data_transformation=Data_Transformation(config.get_data_transformation_config())
        data_transform.data_transforamtion()

if __name__=="__main__":
    try:
        logger.info(">>>>>>>STAGE: DATA TRANSFORMATION STARTED<<<<<<<<< ")
        config=ConfigurationManager()
        data_transformed_config=config.get_data_transformation_config()
        data_transform=Data_Transformation(config=data_transformed_config)
        data_transform.data_transforamtion()
        logger.info(">>>>>>>STAGE: DATA TRANSFORMATION ENDED<<<<<<<<< ")

    except Exception as e:
        logger.exception(e)
        raise e