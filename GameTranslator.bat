@echo off
:: Cek apakah sudah admin
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :run
) else (
    echo Meminta izin Administrator...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit
)

:run
:: Ubah direktori ke lokasi foldermu
cd /d "C:\Users\Rois Adhi Assadad\Desktop\GameTranslator"

:: Jalankan python
"C:\Users\Rois Adhi Assadad\AppData\Local\Python\bin\python.exe" main.py
pause