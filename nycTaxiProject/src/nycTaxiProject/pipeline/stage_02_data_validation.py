from nycTaxiProject.components.data_validation import Data_Validation
from nycTaxiProject.config.configuration import ConfigurationManager
from nycTaxiProject import logger

STAGE_NAME="Data Validation Stage"

class DataValidationPipeline:
    def __init__(self):
        pass
    def main(self):
        config=ConfigurationManager()
        data_validation=Data_Validation(config.get_data_validation_config())
        data_validation.validation_all_columns()

if __name__=="__main__":
    try:
        logger.info(f">>>>>>>>>>{STAGE_NAME} STARTED<<<<<<<<<<")
        obj=DataValidationPipeline
        obj.main()
        logger.info(f">>>>>>>>>>{STAGE_NAME} COMPLETED<<<<<<<<<<")
    
    except Exception as e:
        logger.exception(e)
        raise e