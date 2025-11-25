#include <stdio.h>

// Простая структура для демонстрации
typedef struct {
    char message[50];
    int counter;
} demo_data_t;

// Простая задержка
void delay() {
    for (volatile int i = 0; i < 500000; i++);
}

int main() {
    printf("=== STM32 IoT Device in Renode ===\n");
    printf("=== hello artem ===\n\n");
    
    demo_data_t data = {
        .message = "hello artem from STM32",
        .counter = 0
    };
    
    while (1) {
        // Выводим сообщение
        printf("MESSAGE: \"%s\"\n", data.message);
        printf("COUNTER: %d\n", data.counter);
        
        // Также выводим JSON данные (как в реальной системе)
        printf("SENSOR_DATA: {\"device_id\":1234567890,\"timestamp\":%d,\"message\":\"%s\"}\n", 
               data.counter * 1000, data.message);
        
        data.counter++;
        printf("---\n");
        delay();
    }
    
    return 0;
}