import json
from datetime import datetime

def validate_sensor_data(data):
    """Валидация данных сенсора"""
    required_fields = ['device_id', 'timestamp', 'temperature', 'humidity', 'pressure', 'status']
    
    if not all(field in data for field in required_fields):
        return False, "Missing required fields"
    
    try:
        # Проверка типов данных
        int(data['device_id'])
        int(data['timestamp'])
        float(data['temperature'])
        float(data['humidity'])
        int(data['pressure'])
        int(data['status'])
    except (ValueError, TypeError):
        return False, "Invalid data types"
    
    # Проверка диапазонов
    if not (-50 <= data['temperature'] <= 100):
        return False, "Temperature out of range"
    
    if not (0 <= data['humidity'] <= 100):
        return False, "Humidity out of range"
    
    if not (800 <= data['pressure'] <= 1200):
        return False, "Pressure out of range"
    
    return True, "Valid"

def format_timestamp(timestamp):
    """Форматирование timestamp в читаемую дату"""
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "Invalid timestamp"