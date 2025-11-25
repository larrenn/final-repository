// Прошивка для вывода в UART Renode
// Используем семихостинг для работы с UART

// Функция для записи в UART (семихостинг)
void _write_uart(const char *str) {
    // В Renode UART обычно на адресе 0x40000000
    volatile char *uart = (volatile char*)0x40000000;
    
    while (*str) {
        *uart = *str;
        str++;
    }
}

// Главная функция
int main() {
    // Выводим сообщение в UART
    _write_uart("=== STM32 IoT Device in Renode ===\r\n");
    _write_uart("=== hello artem ===\r\n");
    _write_uart("\r\n");
    
    int counter = 0;
    
    while (1) {
        // Выводим данные в UART
        _write_uart("MESSAGE: \"hello artem from STM32\"\r\n");
        
        // Простой счетчик
        char counter_str[10];
        char *p = counter_str;
        int n = counter;
        do {
            *p++ = '0' + n % 10;
            n /= 10;
        } while (n > 0);
        *p-- = '\0';
        
        // Переворачиваем строку
        char *q = counter_str;
        while (q < p) {
            char temp = *q;
            *q = *p;
            *p = temp;
            q++;
            p--;
        }
        
        _write_uart("COUNTER: ");
        _write_uart(counter_str);
        _write_uart("\r\n");
        
        _write_uart("SENSOR_DATA: {\"device_id\":1234567890,\"timestamp\":");
        
        // Выводим timestamp
        char ts_str[10];
        p = ts_str;
        n = counter * 1000;
        do {
            *p++ = '0' + n % 10;
            n /= 10;
        } while (n > 0);
        *p-- = '\0';
        
        // Переворачиваем
        q = ts_str;
        while (q < p) {
            char temp = *q;
            *q = *p;
            *p = temp;
            q++;
            p--;
        }
        
        _write_uart(ts_str);
        _write_uart(",\"message\":\"hello artem from STM32\"}\r\n");
        _write_uart("---\r\n");
        
        counter++;
        
        // Простая задержка
        for (volatile int i = 0; i < 1000000; i++);
    }
    
    return 0;
}