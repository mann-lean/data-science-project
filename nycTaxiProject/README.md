End to end NYC taxi

### DagsHub
# set environment variables for MLFLOW
os.environ["MLFLOW_TRACKING_URI"]="https://dagshub.com/mann-lean/data-science-project.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"]="mann-lean"


$env:MLFLOW_TRACKING_URI = "https://dagshub.com/mann-lean/data-science-project.mlflow"

$env:MLFLOW_TRACKING_USERNAME = "mann-lean"

### DVC 
dvc init (It will intialize DVC directory)
dvc repro (It will run dvc.yaml file & create dvc.lock file ,which file stores every data version stored in it)