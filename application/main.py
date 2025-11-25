#!/usr/bin/env python3
import threading
import time
import json
import signal
import sys
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
        
        # Настройка обработки Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        """Обработчик сигналов для корректного завершения"""
        print(f"\nReceived signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)
        
    def initialize(self):
        """Инициализация всех компонентов системы"""
        print("=== Initializing IoT Data Processing System ===")
        
        try:
            # 1. База данных
            self.db_manager = DatabaseManager(self.settings.DATABASE_URL)
            self.db_manager.initialize()
            print("✓ Database initialized")
            
            # 2. RabbitMQ
            self.mqtt_manager = MQTTManager(
                host=self.settings.RABBITMQ_HOST,
                port=self.settings.RABBITMQ_PORT
            )
            self.mqtt_manager.connect()
            print("✓ RabbitMQ connected")
            
            # 3. TCP сервер для приема данных
            self.tcp_server = TCPServer(
                host=self.settings.TCP_SERVER_HOST,
                port=self.settings.TCP_SERVER_PORT,
                on_data_received=self.handle_sensor_data
            )
            print("✓ TCP server configured")
            
            # 4. Менеджер синхронизации
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
            
            # Сохраняем в базу данных (помечаем как несинхронизированное)
            record_id = self.db_manager.save_sensor_data(sensor_data)
            print(f"✓ Data received from device {sensor_data['device_id']} (ID: {record_id})")
            
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
        print("Press Ctrl+C to stop the system")
        
        try:
            # Запуск TCP сервера в отдельном потоке
            tcp_thread = threading.Thread(target=self.tcp_server.start, name="TCP-Server")
            tcp_thread.daemon = True
            tcp_thread.start()
            print("✓ TCP server started")
            
            # Запуск синхронизации в отдельном потоке
            sync_thread = threading.Thread(target=self.sync_manager.start, name="Sync-Manager")
            sync_thread.daemon = True
            sync_thread.start()
            print("✓ Sync manager started")
            
            print("✓ System fully operational with RabbitMQ!")
            print("Waiting for incoming connections...")
            
            # Основной цикл с улучшенной обработкой
            self._main_loop()
            
        except Exception as e:
            print(f"System error: {e}")
        finally:
            self.stop()
    
    def _main_loop(self):
        """Основной цикл приложения"""
        stats_counter = 0
        
        while self.running:
            try:
                # Показываем статистику каждые 10 итераций (примерно каждые 10 секунд)
                if stats_counter % 10 == 0:
                    stats = self.db_manager.get_statistics()
                    print(f"📊 Database stats - Total: {stats['total']}, Unsynced: {stats['unsynced']}, Devices: {stats['unique_devices']}")
                
                stats_counter += 1
                time.sleep(1)  # Уменьшаем задержку для более отзывчивого Ctrl+C
                
            except KeyboardInterrupt:
                print("\n🛑 Keyboard interrupt received")
                break
            except Exception as e:
                print(f"Main loop error: {e}")
                time.sleep(5)
    
    def stop(self):
        """Корректная остановка системы"""
        if not self.running:
            return
            
        print("🛑 Stopping IoT system...")
        self.running = False
        
        if self.tcp_server:
            self.tcp_server.stop()
        if self.sync_manager:
            self.sync_manager.stop()
        if self.mqtt_manager:
            self.mqtt_manager.disconnect()
        if self.db_manager:
            self.db_manager.close()
        
        print("✅ System stopped gracefully")

if __name__ == "__main__":
    app = IoTApplication()
    
    try:
        app.initialize()
        app.start()
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted during initialization")
        app.stop()
    except Exception as e:
        print(f"❌ Application failed to start: {e}")
        app.stop()