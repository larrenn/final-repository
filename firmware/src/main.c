#include "main.h"
#include "sensors.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Простая реализация printf для Renode
int _write(int file, char *ptr, int len) {
    for (int i = 0; i < len; i++) {
        // Эмуляция UART вывода - в Renode это будет видно в терминале
        // В реальном устройстве здесь был бы код для UART
    }
    return len;
}

// Эмуляция задержки
void delay_ms(uint32_t ms) {
    // В Renode это эмулируется
}

int main(void) {
    // Инициализация
    printf("=== IoT Device Started ===\n");
    
    device_data_t sensor_data;
    uint32_t packet_count = 0;
    
    printf("Device ID: 0x%08lX\n", generate_device_id());
    printf("Starting data transmission...\n");
    
    while (1) {
        // Чтение данных с датчиков
        read_sensor_data(&sensor_data);
        
        // Формирование JSON для отправки
        printf("SENSOR_DATA: {\"device_id\":%lu,\"timestamp\":%lu,\"temperature\":%.2f,\"humidity\":%.2f,\"pressure\":%d,\"status\":%d}\n",
               sensor_data.device_id, sensor_data.timestamp, sensor_data.temperature,
               sensor_data.humidity, sensor_data.pressure, sensor_data.status);
        
        packet_count++;
        
        // Задержка 5 секунд
        delay_ms(5000);
    }
    
    return 0;
}