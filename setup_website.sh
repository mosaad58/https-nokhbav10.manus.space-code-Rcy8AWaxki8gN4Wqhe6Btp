#!/bin/bash

# Al-Nokhba International Trading Website Setup Script
# سكريبت إعداد موقع النخبة للتجارة الدولية

echo "==================================="
echo "Al-Nokhba Website Setup Script"
echo "سكريبت إعداد موقع النخبة للتجارة الدولية"
echo "==================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    echo "❌ Python 3 غير مثبت. يرجى تثبيت Python 3.8+ أولاً."
    exit 1
fi

echo "✅ Python 3 found"
echo "✅ تم العثور على Python 3"

# Create virtual environment
echo "📦 Creating virtual environment..."
echo "📦 إنشاء البيئة الافتراضية..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
echo "🔧 تفعيل البيئة الافتراضية..."
source venv/bin/activate

# Install requirements
echo "📥 Installing requirements..."
echo "📥 تثبيت المتطلبات..."
cd nokhba_website/nokhba_trade_flask
pip install -r requirements.txt

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ Requirements installed successfully"
    echo "✅ تم تثبيت المتطلبات بنجاح"
else
    echo "❌ Failed to install requirements"
    echo "❌ فشل في تثبيت المتطلبات"
    exit 1
fi

echo ""
echo "🎉 Setup completed successfully!"
echo "🎉 تم الإعداد بنجاح!"
echo ""
echo "To run the website:"
echo "لتشغيل الموقع:"
echo "1. cd nokhba_website/nokhba_trade_flask/src"
echo "2. python main.py"
echo ""
echo "Then open your browser and go to: http://localhost:5000"
echo "ثم افتح المتصفح وانتقل إلى: http://localhost:5000"
echo ""
echo "==================================="

