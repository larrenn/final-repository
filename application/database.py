import sqlite3
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self, database_url='iot_data.db'):
        self.database_url = database_url
        self.connection = None
        
    def initialize(self):
        """Инициализация базы данных"""
        self.connection = sqlite3.connect(self.database_url, check_same_thread=False)
        self._create_tables()
        
    def _create_tables(self):
        """Создание таблиц"""
        cursor = self.connection.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER NOT NULL,
                timestamp INTEGER NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                pressure INTEGER NOT NULL,
                status INTEGER NOT NULL,
                received_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                synced BOOLEAN DEFAULT FALSE
            )
        ''')
        
        self.connection.commit()
    
    def save_sensor_data(self, data):
        """Сохранение данных сенсора в базу"""
        cursor = self.connection.cursor()
        
        cursor.execute('''
            INSERT INTO sensor_data 
            (device_id, timestamp, temperature, humidity, pressure, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['device_id'],
            data['timestamp'],
            data['temperature'],
            data['humidity'],
            data['pressure'],
            data['status']
        ))
        
        self.connection.commit()
        record_id = cursor.lastrowid
        print(f"✓ Data saved to database from device {data['device_id']} (ID: {record_id})")
        return record_id
    
    def get_unsynced_data(self, limit=100):
        """Получение несинхронизированных данных"""
        cursor = self.connection.cursor()
        
        cursor.execute('''
            SELECT * FROM sensor_data 
            WHERE synced = FALSE 
            ORDER BY timestamp ASC 
            LIMIT ?
        ''', (limit,))
        
        columns = [col[0] for col in cursor.description]
        data = []
        
        for row in cursor.fetchall():
            data.append(dict(zip(columns, row)))
        
        return data
    
    def mark_as_synced(self, record_ids):
        """Пометить записи как синхронизированные"""
        if not record_ids:
            return
            
        cursor = self.connection.cursor()
        placeholders = ','.join('?' * len(record_ids))
        
        cursor.execute(f'''
            UPDATE sensor_data 
            SET synced = TRUE 
            WHERE id IN ({placeholders})
        ''', record_ids)
        
        self.connection.commit()
        print(f"✓ Marked {len(record_ids)} records as synced")
    
    def delete_old_synced_data(self, hours=1):
        """Удаление старых синхронизированных данных"""
        cursor = self.connection.cursor()
        
        cursor.execute('''
            DELETE FROM sensor_data 
            WHERE synced = TRUE 
            AND received_at < datetime('now', ?)
        ''', (f'-{hours} hours',))
        
        deleted_count = cursor.rowcount
        self.connection.commit()
        
        return deleted_count
    
    def get_statistics(self):
        """Получение статистики базы данных"""
        cursor = self.connection.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM sensor_data')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM sensor_data WHERE synced = FALSE')
        unsynced = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT device_id) FROM sensor_data')
        unique_devices = cursor.fetchone()[0]
        
        return {
            'total': total,
            'unsynced': unsynced,
            'unique_devices': unique_devices
        }
    
    def close(self):
        """Закрытие соединения с базой"""
        if self.connection:
            self.connection.close()