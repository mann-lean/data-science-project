End to end NYC taxi

### DagsHub
# set environment variables for MLFLOW
os.environ["MLFLOW_TRACKING_URI"]="https://dagshub.com/mann-lean/data-science-project.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"]="mann-lean"


$env:MLFLOW_TRACKING_URI = "https://dagshub.com/mann-lean/data-science-project.mlflow"

$env:MLFLOW_TRACKING_USERNAME = "mann-lean"

### DVC 
dvc init --subdir (It will intialize DVC directory , one leve; up for DVC Initialization)
dvc repro (It will run dvc.yaml file & create dvc.lock file ,which file stores or tracks every data version stored in it)
dvc dag (Graphical structure ,dependency pipeline)
DVC Directed Acyclic Graph (DAG)  proves your architecture is flawless:

data_ingestion is the root. Everything flows from here.

data_validation depends on ingestion.

data_transformation depends on both ingestion and validation. (This proves your "Circuit Breaker" is perfectly wired up!).

model_training depends on transformation.

model_evaluation depends on both transformation (for the test data) and training (for the .pkl model).

(Note: Make sure you ,don't include files (dvc.ignore,dvc.lock) into git . Only keep dvc.yaml file ) 