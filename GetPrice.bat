@echo off
REM รัน main.py ด้วย python
python main.py

REM ตรวจสอบว่าการรัน python สำเร็จหรือไม่
IF %ERRORLEVEL% NEQ 0 (
    echo Python script failed. Exiting...
    pause
    exit /b %ERRORLEVEL%
)

REM ไปยังโฟลเดอร์ของโปรเจกต์ Git
cd path\to\your\project

REM เพิ่มไฟล์ที่มีการเปลี่ยนแปลงทั้งหมด
git add .

REM ตั้งค่า user ถ้าจำเป็น (เฉพาะครั้งแรก)
REM git config user.email "youremail@example.com"
REM git config user.name "YourName"

REM สร้าง commit และ push ขึ้น remote
git commit -m "Update from script run"
git push origin main

pause
