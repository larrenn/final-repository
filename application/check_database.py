#!/usr/bin/env python3
import sqlite3
import os

def check_database():
    """Проверка содержимого базы данных"""
    db_file = 'iot_data.db'
    
    if not os.path.exists(db_file):
        print("❌ Database file not found")
        return
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Проверяем таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("📊 Database Tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Проверяем данные в sensor_data
        cursor.execute("SELECT COUNT(*) as total FROM sensor_data;")
        total_records = cursor.fetchone()[0]
        print(f"📈 Total records in sensor_data: {total_records}")
        
        if total_records > 0:
            cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT 3;")
            records = cursor.fetchall()
            print(f"📋 Last {len(records)} records:")
            for record in records:
                print(f"  ID: {record[0]}, Device: {record[1]}, Temp: {record[3]}°C")
        
        # Проверяем статистику по устройствам
        cursor.execute("SELECT COUNT(DISTINCT device_id) FROM sensor_data;")
        unique_devices = cursor.fetchone()[0]
        print(f"📱 Unique devices: {unique_devices}")
        
        conn.close()
        print("✅ Database check completed")
        
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    check_database()