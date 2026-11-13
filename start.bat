@echo off
title IELTS Mock TMA & Bot
echo ========================================================
echo   IELTS Computer-Delivered Mock Platform & Bot
echo ========================================================
echo.
echo Server va Telegram Bot ishga tushirilmoqda...
echo.
if exist "C:\Program Files\Python311\python.exe" (
    "C:\Program Files\Python311\python.exe" run.py
) else (
    py run.py
)
pause
