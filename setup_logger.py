import logging

log_format = "%(asctime)s | %(levelname)s | %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)
logger = logging.getLogger('base logger')
# logger.setLevel(logging.INFO)



