#!/usr/bin/env python3
import threading
import time
import json
from database import DatabaseManager
from mqtt_handler import MQTTManager
from sync_manager import SyncManager
from tcp_server import TCPServer
from config.settings import Settings

class IoTApplication:
    def __init__(self):
        self.settings = Settings()
        self.running = False
        
        self.db_manager = None
        self.mqtt_manager = None
        self.tcp_server = None
        self.sync_manager = None
        
    def initialize(self):
        """Инициализация всех компонентов системы"""
        print("=== Initializing IoT Data Processing System ===")
        
        try:
            self.db_manager = DatabaseManager(self.settings.DATABASE_URL)
            self.db_manager.initialize()
            print("✓ Database initialized")
            
            self.mqtt_manager = MQTTManager(
                host=self.settings.RABBITMQ_HOST,
                port=self.settings.RABBITMQ_PORT
            )
            self.mqtt_manager.connect()
            print("✓ RabbitMQ connected")
            
            self.tcp_server = TCPServer(
                host=self.settings.TCP_SERVER_HOST,
                port=self.settings.TCP_SERVER_PORT,
                on_data_received=self.handle_sensor_data
            )
            print("✓ TCP server configured")
            
            self.sync_manager = SyncManager(
                db_manager=self.db_manager,
                mqtt_manager=self.mqtt_manager,
                sync_interval=self.settings.SYNC_INTERVAL
            )
            print("✓ Sync manager initialized")
            
            self.running = True
            print("✓ All components initialized successfully")
            
        except Exception as e:
            print(f"✗ Initialization failed: {e}")
            raise
    
    def handle_sensor_data(self, data_json, client_address):
        """Обработка входящих данных с датчиков"""
        try:
            sensor_data = json.loads(data_json)
            
            required_fields = ['device_id', 'timestamp', 'temperature', 'humidity', 'pressure', 'status']
            if not all(field in sensor_data for field in required_fields):
                print(f"Invalid data format from {client_address}")
                return
            
            self.db_manager.save_sensor_data(sensor_data)
            print(f"✓ Data saved from device {sensor_data['device_id']}")
            
        except json.JSONDecodeError as e:
            print(f"JSON decode error from {client_address}: {e}")
        except Exception as e:
            print(f"Error processing data from {client_address}: {e}")
    
    def start(self):
        """Запуск системы"""
        if not self.running:
            print("System not initialized")
            return
        
        print("=== Starting IoT System ===")
        
        try:
            tcp_thread = threading.Thread(target=self.tcp_server.start)
            tcp_thread.daemon = True
            tcp_thread.start()
            print("✓ TCP server started")
            
            sync_thread = threading.Thread(target=self.sync_manager.start)
            sync_thread.daemon = True
            sync_thread.start()
            print("✓ Sync manager started")
            
            self._main_loop()
            
        except KeyboardInterrupt:
            print("\nShutting down...")
        except Exception as e:
            print(f"System error: {e}")
        finally:
            self.stop()
    
    def _main_loop(self):
        """Основной цикл приложения"""
        while self.running:
            try:
                stats = self.db_manager.get_statistics()
                print(f"Database stats - Total: {stats['total']}, Unsynced: {stats['unsynced']}, Devices: {stats['unique_devices']}")
                
                time.sleep(10)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Main loop error: {e}")
                time.sleep(5)
    
    def stop(self):
        """Корректная остановка системы"""
        print("Stopping IoT system...")
        self.running = False
        
        if self.tcp_server:
            self.tcp_server.stop()
        if self.sync_manager:
            self.sync_manager.stop()
        if self.mqtt_manager:
            self.mqtt_manager.disconnect()
        
        print("System stopped")

if __name__ == "__main__":
    app = IoTApplication()
    
    try:
        app.initialize()
        app.start()
    except Exception as e:
        print(f"Application failed to start: {e}")