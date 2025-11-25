import logging
import sys
from config.settings import Settings

def setup_logger():
    """Настройка логгера"""
    settings = Settings()
    
    logger = logging.getLogger('iot_system')
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler('iot_system.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger