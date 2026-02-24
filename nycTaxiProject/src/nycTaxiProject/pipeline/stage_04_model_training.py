from nycTaxiProject.components.model_training import Model_Trainer
from nycTaxiProject.config.configuration import ConfigurationManager
from nycTaxiProject import logger

STAGE_NAME="MODEL TRAINING STAGE"

class ModelTrainingPipeline:
    def __init__(self):
        pass
    def main(self):
        logger.info(">>>>>>>STAGE: MODEL TRAINING STARTED<<<<<<<<< ")
        config=ConfigurationManager()
        model_training_config=config.get_model_training_config()
        model_training=Model_Trainer(config=model_training_config)
        model_training.train_model()
        logger.info(">>>>>>>STAGE: MODEL TRAINING ENDED<<<<<<<<< ")

if __name__=="__main__":
    try:
        obj=ModelTrainingPipeline()
        obj.main()

    except Exception as e:
        logger.exception(e)
        raise e