import pika
import json
from config.settings import Settings

class MQTTManager:
    def __init__(self, host='localhost', port=5672):
        self.settings = Settings()
        self.host = host
        self.port = port
        self.connection = None
        self.channel = None
        self.connected = False
        
    def connect(self):
        """Подключение к RabbitMQ"""
        try:
            credentials = pika.PlainCredentials(
                self.settings.RABBITMQ_USER,
                self.settings.RABBITMQ_PASS
            )
            
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    credentials=credentials
                )
            )
            
            self.channel = self.connection.channel()
            
            # Объявление очереди
            self.channel.queue_declare(
                queue='sensor_data',
                durable=True
            )
            
            self.connected = True
            print("✓ Connected to RabbitMQ")
            
        except Exception as e:
            print(f"✗ RabbitMQ connection failed: {e}")
            self.connected = False
            raise
    
    def publish_data(self, data):
        """Публикация данных в RabbitMQ"""
        if not self.connected:
            raise ConnectionError("Not connected to RabbitMQ")
        
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key='sensor_data',
                body=json.dumps(data),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # persistent
                    content_type='application/json'
                )
            )
            return True
            
        except Exception as e:
            print(f"Publish error: {e}")
            self.connected = False
            return False
    
    def is_connected(self):
        """Проверка подключения"""
        return self.connected and (not self.connection or not self.connection.is_closed)
    
    def disconnect(self):
        """Отключение от RabbitMQ"""
        try:
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            self.connected = False
            print("RabbitMQ disconnected")
        except Exception as e:
            print(f"Error disconnecting from RabbitMQ: {e}")