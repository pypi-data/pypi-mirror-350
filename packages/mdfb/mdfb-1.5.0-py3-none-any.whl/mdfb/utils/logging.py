import datetime
import logging
import os

def setup_logging(directory: str):
    log_name = datetime.datetime.now().strftime("mdfb_%d%m%Y_%H%M%S.log")
    logging.basicConfig(
        filename=os.path.join(directory, log_name), 
        encoding='utf-8', 
        level=logging.INFO,
        format='[%(asctime)s] %(message)s', 
        datefmt='%m/%d/%Y %I:%M:%S %p',
    )