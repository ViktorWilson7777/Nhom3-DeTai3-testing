@echo off
chcp 65001 > nul
echo ========================================================
echo   DANG CHAY KIEM THU & XUAT BAO CAO JACOCO...
echo ========================================================
call "C:\Users\ADMIN\.m2\wrapper\dists\apache-maven-3.9.9\8e74001100ff70d6af083c5511fcc5ec49282d7017cde82c3698eee8fdf86698\bin\mvn.cmd" clean test

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo   TEST THANH CONG! DANG MO BAO CAO JACOCO TRONG BROWSER...
    echo ========================================================
    start "" target\site\jacoco\index.html
) else (
    echo.
    echo [ERROR] Co loi xay ra trong luc chay test. Vui long kiem tra log o tren!
)
echo.
pause
