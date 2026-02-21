from nycTaxiProject import logger
from nycTaxiProject.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from nycTaxiProject.pipeline.stage_02_data_validation import DataValidationPipeline

STAGE_NAME="DATA INGESTION STAGE"
try:
    logger.info(f">>>>>>Stage {STAGE_NAME} started <<<<<<<")
    data_ingestion=DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f">>>>>>Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME="DATA VALIDATION STAGE"
try:
    logger.info(f">>>>>>Stage {STAGE_NAME} started <<<<<<<")
    data_ingestion=DataValidationPipeline()
    data_ingestion.main()
    logger.info(f">>>>>>Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e
