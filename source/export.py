import logging
import logging.handlers
import configparser
import json

# Read config
config = configparser.ConfigParser()
config.read('config.ini')

# Setup logger
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)

for ip in json.loads(config["Export"]["export_to"]):
    handler = logging.handlers.SysLogHandler(address=(ip, 514))
    logger.addHandler(handler)


def export_report(log: dict):
    logger.info(log)

