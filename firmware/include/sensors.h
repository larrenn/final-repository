#ifndef SENSORS_H
#define SENSORS_H

#include <stdint.h>

typedef struct {
    uint32_t device_id;
    uint32_t timestamp;
    float temperature;
    float humidity;
    uint16_t pressure;
    uint8_t status;
} device_data_t;

void read_sensor_data(device_data_t *data);
uint32_t generate_device_id(void);

#endif