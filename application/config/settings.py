import os
from dotenv import load_dotenv

# Загружаем переменные окружения из корневой папки
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

class Settings:
    # Настройки TCP сервера
    TCP_SERVER_HOST = os.getenv('TCP_SERVER_HOST', '0.0.0.0')
    TCP_SERVER_PORT = int(os.getenv('TCP_SERVER_PORT', '8080'))
    
    # Настройки базы данных
    DATABASE_URL = os.getenv('DATABASE_URL', 'iot_data.db')
    
    # Настройки RabbitMQ
    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
    RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', '5672'))
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'admin')
    RABBITMQ_PASS = os.getenv('RABBITMQ_PASS', 'password')
    
    # Настройки синхронизации
    SYNC_INTERVAL = int(os.getenv('SYNC_INTERVAL', '30'))
    DELETE_AFTER_HOURS = int(os.getenv('DELETE_AFTER_HOURS', '1'))
    
    # Другие настройки
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')