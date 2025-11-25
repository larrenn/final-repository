#include "sensors.h"
#include <stdlib.h>

static uint32_t device_unique_id = 0;

uint32_t generate_device_id(void) {
    if (device_unique_id == 0) {
        // Генерация "уникального" ID
        device_unique_id = 0x42000000 + (rand() & 0xFFFF);
    }
    return device_unique_id;
}

void read_sensor_data(device_data_t *data) {
    static uint32_t counter = 0;
    
    data->device_id = generate_device_id();
    data->timestamp = counter * 10000; // Эмуляция timestamp
    data->temperature = 20.0f + (counter % 150) * 0.1f;
    data->humidity = 30.0f + (counter % 500) * 0.1f;
    data->pressure = 1000 + (counter % 30);
    data->status = (counter % 10 == 0) ? 0x00 : 0x01; // Иногда ошибка
    
    counter++;
}