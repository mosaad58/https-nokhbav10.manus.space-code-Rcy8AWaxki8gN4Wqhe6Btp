@echo off
REM Al-Nokhba International Trading Website Setup Script for Windows
REM سكريبت إعداد موقع النخبة للتجارة الدولية لنظام Windows

echo ===================================
echo Al-Nokhba Website Setup Script
echo سكريپت إعداد موقع النخبة للتجارة الدولية
echo ===================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    echo ❌ Python غير مثبت. يرجى تثبيت Python 3.8+ أولاً.
    pause
    exit /b 1
)

echo ✅ Python found
echo ✅ تم العثور على Python

REM Create virtual environment
echo 📦 Creating virtual environment...
echo 📦 إنشاء البيئة الافتراضية...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
echo 🔧 تفعيل البيئة الافتراضية...
call venv\Scripts\activate.bat

REM Install requirements
echo 📥 Installing requirements...
echo 📥 تثبيت المتطلبات...
cd nokhba_website\nokhba_trade_flask
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install requirements
    echo ❌ فشل في تثبيت المتطلبات
    pause
    exit /b 1
)

echo.
echo 🎉 Setup completed successfully!
echo 🎉 تم الإعداد بنجاح!
echo.
echo To run the website:
echo لتشغيل الموقع:
echo 1. cd nokhba_website\nokhba_trade_flask\src
echo 2. python main.py
echo.
echo Then open your browser and go to: http://localhost:5000
echo ثم افتح المتصفح وانتقل إلى: http://localhost:5000
echo.
echo ===================================
pause

