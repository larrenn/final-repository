#!/usr/bin/env python3
import socket
import json
import time
import random

def test_sensor_data():
    """Генерация тестовых данных сенсора"""
    return {
        "device_id": random.randint(1000000000, 9999999999),
        "timestamp": int(time.time()),
        "temperature": round(20 + random.random() * 10, 2),
        "humidity": round(30 + random.random() * 40, 2),
        "pressure": 1000 + random.randint(0, 30),
        "status": 1
    }

def send_test_data(host='localhost', port=8080, count=5):
    """Отправка тестовых данных на TCP сервер"""
    
    for i in range(count):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))
            
            sensor_data = test_sensor_data()
            message = json.dumps(sensor_data) + '\n'
            client_socket.send(message.encode('utf-8'))
            
            print(f"Sent: {sensor_data}")
            client_socket.close()
            
            time.sleep(2)
            
        except Exception as e:
            print(f"Error sending data: {e}")
            break

if __name__ == "__main__":
    print("Starting test client...")
    send_test_data(count=5)
    print("Test completed")