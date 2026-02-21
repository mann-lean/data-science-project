from nycTaxiProject import logger
from nycTaxiProject.pipeline.stage_01_data_ingestion import DataIngestionPipeline

STAGE_NAME="DATA INGESTION STAGE"
try:
    logger.info(f">>>>>>Stage {STAGE_NAME} started <<<<<<<")
    data_ingestion=DataIngestionPipeline()
    data_ingestion.main()
    logger.info(f">>>>>>Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e