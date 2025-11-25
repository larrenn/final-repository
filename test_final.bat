@echo off
echo === FINAL IoT SYSTEM TEST ===
echo.

echo [1/4] Starting RabbitMQ...
docker-compose up -d
timeout /t 3
echo.

echo [2/4] Starting Main Application...
cd application
start cmd /k "python main.py"
timeout /t 5
echo.

echo [3/4] Testing Data Pipeline...
python test_client.py
timeout /t 2
python check_database.py
echo.

echo [4/4] Test Complete!
echo.
echo ✅ Check main.py window for data processing
echo ✅ Check database results above
echo ✅ Check RabbitMQ: http://localhost:15672
echo.
pause