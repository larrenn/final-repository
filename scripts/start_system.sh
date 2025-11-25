#!/bin/bash

echo "=== Starting IoT System ==="

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Запуск RabbitMQ
echo "Starting RabbitMQ..."
docker-compose up -d rabbitmq

# Ожидание запуска RabbitMQ
echo "Waiting for RabbitMQ to start..."
sleep 10

# Проверка PlatformIO
if ! command -v pio &> /dev/null; then
    echo "PlatformIO is not installed. Please install it first."
    exit 1
fi

# Сборка прошивки
echo "Building firmware..."
cd firmware
pio run

if [ $? -eq 0 ]; then
    echo "Firmware built successfully"
else
    echo "Firmware build failed"
    exit 1
fi

cd ..

# Запуск Python приложения
echo "Starting Python application..."
cd application
python main.py &
APP_PID=$!

cd ..

echo "=== System started ==="
echo "RabbitMQ: localhost:15672 (admin/password)"
echo "TCP Server: localhost:8080"
echo "Application PID: $APP_PID"
echo ""
echo "Press Ctrl+C to stop the system"

# Ожидание сигнала остановки
trap "kill $APP_PID; docker-compose down; echo 'System stopped'; exit" INT
wait