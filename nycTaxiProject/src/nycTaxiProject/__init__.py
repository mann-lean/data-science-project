import os 
import sys
import logging

logging_str="[%(asctime)s : %(levelname)s : %(module)s : %(message)s]" # why we pu list in a string? because we want to format the log messages in a specific way. The list is used to specify the format of the log messages. The %(asctime)s will be replaced with the time when the log message was created, %(levelname)s will be replaced with the level of the log message (e.g. INFO, ERROR), %(module)s will be replaced with the name of the module where the log message was created, and %(message)s will be replaced with the actual log message.

log_dir="logs"
log_filepath=os.path.join(log_dir,"running_logs.log")
os.makedirs(log_dir,exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[logging.FileHandler(log_filepath),
              logging.StreamHandler(sys.stdout)
              ]
)
logger=logging.getLogger("nycTaxiProjectLogger")
