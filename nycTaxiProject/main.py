from nycTaxiProject import logger
from nycTaxiProject.pipeline.stage_01_data_ingestion import DataIngestionPipeline
from nycTaxiProject.pipeline.stage_02_data_validation import DataValidationPipeline
from nycTaxiProject.pipeline.stage_03_data_transformation import DataTransformationPipeline
from nycTaxiProject.pipeline.stage_04_model_training import ModelTrainingPipeline
from nycTaxiProject.pipeline.stage_05_model_evaluation import ModelEvaluationPipeline

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

STAGE_NAME="DATA TRANSFORMATION STAGE"
try:
    logger.info(f">>>>>>Stage {STAGE_NAME} started <<<<<<<")
    data_transformation=DataTransformationPipeline()
    data_transformation.main()
    logger.info(f">>>>>>Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME="MODEL TRAINING STAGE"
try:
    logger.info(f">>>>>>Stage {STAGE_NAME} started <<<<<<<")
    data_transformation=ModelTrainingPipeline()
    data_transformation.main()
    logger.info(f">>>>>>Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME="MODEL EVALUATION STAGE"
try:
    logger.info(f">>>>>>Stage {STAGE_NAME} started <<<<<<<")
    data_transformation=ModelEvaluationPipeline()
    data_transformation.main()
    logger.info(f">>>>>>Stage {STAGE_NAME} completed <<<<<<<\n\nx==========x")
except Exception as e:
    logger.exception(e)
    raise e
