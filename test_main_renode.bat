@echo off
echo =================================
echo   Testing main_renode.c
echo =================================
echo.

echo [1/4] Checking file...
if exist firmware\src\main_renode.c (
    echo  main_renode.c found
) else (
    echo  main_renode.c not found
    goto end
)

echo.
echo [2/4] Compiling for Windows test...
gcc -o test_main_renode.exe firmware/src/main_renode.c 2>nul

if exist test_main_renode.exe (
    echo  Compiled successfully
    echo.
    echo [3/4] Running test...
    echo OUTPUT:
    echo --------
    test_main_renode.exe
) else (
    echo  GCC not available, showing file content:
    echo.
    type firmware\src\main_renode.c
)

:end
echo.
echo [4/4] Test completed
del test_main_renode.exe 2>nul
pause
