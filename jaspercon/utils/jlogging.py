import logging
from logging.handlers import RotatingFileHandler
from os import path, mkdir

def _initialize_logging(log_path: str) -> None:
    if not path.exists(log_path):
        mkdir(log_path)
        
def get_logger(app_name: str, module_name: str, debug: bool = False, log_path: str = 'logs') -> logging.Logger:
    _initialize_logging(log_path)
    
    logger = logging.getLogger(name=f"{app_name}.{module_name}")
    logger.setLevel(logging.DEBUG if debug else logging.INFO)
    
    log_file_name = f"{app_name}.{module_name}.log"
    log_file_path = path.join(log_path, log_file_name)
    
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = RotatingFileHandler(filename=log_file_path, maxBytes=1024, backupCount=30)
    file_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    file_handler.setFormatter(log_formatter)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
    console_handler.setFormatter(log_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger
    
    