from nycTaxiProject.components.model_evaluation import Model_Evaluation
from nycTaxiProject.config.configuration import ConfigurationManager
from nycTaxiProject import logger
import pandas as pd

STAGE_NAME="MODEL EVALUATION STAGE"

class ModelEvaluationPipeline:
    def __init__(self):
        pass
    def main(self):
        try:
            logger.info(">>>>>>>STAGE: MODEL EVALUATION Started<<<<<<<<< ")
            config=ConfigurationManager()
            model_evaluation_config=config.get_model_evaluation()
            x_train=pd.read_csv(model_evaluation_config.x_train_dir)
            y_train=pd.read_csv(model_evaluation_config.y_train_dir)
            x_test=pd.read_csv(model_evaluation_config.x_test_dir)
            y_test=pd.read_csv(model_evaluation_config.y_test_dir)
            model_evaluation=Model_Evaluation(model_evaluation_config)
            model_evaluation.evaluate_model(x_train,y_train,x_test,y_test)
            logger.info(">>>>>>>STAGE: MODEL EVALUATION ENDED<<<<<<<<< ")

        except Exception as e:
            logger.exception(e)
            raise e
        
if __name__=="__main__":
    try:
        obj=ModelEvaluationPipeline()
        obj.main()
    except Exception as e:
        logger.exception(e)
        raise e