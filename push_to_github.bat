@echo off
title GitHubga Push Qilish
color 0b
echo ========================================================
echo   IELTS Mock Platformani GitHubga Yuklash
echo ========================================================
echo.
git -c safe.directory="*" remote remove origin 2>nul
git -c safe.directory="*" remote add origin https://github.com/sardorqarshiyev169-png/ielts-mock-bot.git
git -c safe.directory="*" branch -M main

echo [1/2] GitHubga ulanish va yuklash boshlandi...
echo.
echo DIQQAT: Agar brauzerda oyna ochilsa, "Sign in with your browser" yoki "Authorize" tugmasini bosing!
echo.
git -c safe.directory="*" push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================================
    echo   [MUVAFFAQIYATLI] Barcha fayllar GitHubga yuklandi!
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo   [XATOLIK] Yuklanmadi. Brauzerdan ruxsat berish kerak edi.
    echo ========================================================
)
echo.
pause
