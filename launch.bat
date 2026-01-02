@echo off
chcp 65001 >nul
echo ========================================
echo      CASER Profile Builder
echo ========================================
echo.

REM Устанавливаем библиотеки если их нет
echo Installing required libraries...
pip install customtkinter reportlab pillow --quiet

REM Запускаем приложение
echo Starting application...
python main.py

REM Если скрипт упал
if %errorlevel% neq 0 (
    echo.
    echo Application crashed. Press any key to exit...
    pause >nul
)