from loguru import logger
import sys

def setup_logger():
    logger.remove()  
    logger.add(sys.stdout, level="INFO")
    logger.add("/logs/app.log", level="INFO", rotation="1 week")  

setup_logger()
