@echo off
title IELTS Mini App HTTPS Tunnel
echo ========================================================
echo   Telegram Mini App uchun Bepul HTTPS Havola
echo ========================================================
echo.
echo Telegram Mini App uchun HTTPS havola yaratilmoqda...
echo (Chiqgan "https://...lhr.life" yoki "https://...pinggy.link" havolasini BotFather ga berasiz)
echo.
ssh -R 80:localhost:8080 nokey@localhost.run
pause
