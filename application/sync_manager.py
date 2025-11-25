import time
import threading
from datetime import datetime

class SyncManager:
    def __init__(self, db_manager, mqtt_manager, sync_interval=30):
        self.db_manager = db_manager
        self.mqtt_manager = mqtt_manager
        self.sync_interval = sync_interval
        self.running = False
        self.sync_thread = None
        
    def start(self):
        """Запуск синхронизации"""
        self.running = True
        self.sync_thread = threading.Thread(target=self._sync_loop)
        self.sync_thread.daemon = True
        self.sync_thread.start()
        print(f"Sync manager started (interval: {self.sync_interval}s)")
    
    def _sync_loop(self):
        """Цикл синхронизации"""
        while self.running:
            try:
                self._sync_data()
                self._cleanup_old_data()
                time.sleep(self.sync_interval)
                
            except Exception as e:
                print(f"Sync loop error: {e}")
                time.sleep(10)
    
    def _sync_data(self):
        """Синхронизация данных с RabbitMQ"""
        if not self.mqtt_manager.is_connected():
            print("RabbitMQ not connected, skipping sync")
            return
        
        unsynced_data = self.db_manager.get_unsynced_data(limit=50)
        
        if not unsynced_data:
            return
        
        print(f"Syncing {len(unsynced_data)} records to RabbitMQ...")
        
        successful_syncs = []
        
        for record in unsynced_data:
            try:
                mqtt_data = {
                    'id': record['id'],
                    'device_id': record['device_id'],
                    'timestamp': record['timestamp'],
                    'temperature': record['temperature'],
                    'humidity': record['humidity'],
                    'pressure': record['pressure'],
                    'status': record['status'],
                    'received_at': record['received_at']
                }
                
                if self.mqtt_manager.publish_data(mqtt_data):
                    successful_syncs.append(record['id'])
                    
            except Exception as e:
                print(f"Error syncing record {record['id']}: {e}")
        
        if successful_syncs:
            self.db_manager.mark_as_synced(successful_syncs)
            print(f"✓ Successfully synced {len(successful_syncs)} records")
    
    def _cleanup_old_data(self):
        """Очистка старых данных"""
        try:
            deleted_count = self.db_manager.delete_old_synced_data(hours=1)
            if deleted_count > 0:
                print(f"✓ Cleaned up {deleted_count} old records")
        except Exception as e:
            print(f"Cleanup error: {e}")
    
    def stop(self):
        """Остановка синхронизации"""
        self.running = False
        if self.sync_thread:
            self.sync_thread.join(timeout=5)
        print("Sync manager stopped")