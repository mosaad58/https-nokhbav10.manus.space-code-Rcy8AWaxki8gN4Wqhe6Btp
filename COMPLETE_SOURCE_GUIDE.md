# دليل المصدر الكامل لموقع النخبة للتجارة الدولية
# Complete Source Guide for Al-Nokhba International Trading Website

## 📋 نظرة عامة / Overview

هذا الأرشيف يحتوي على **جميع الملفات المطلوبة** لإعادة بناء والتعديل على موقع النخبة للتجارة الدولية بالكامل.

This archive contains **all required files** to rebuild and modify the Al-Nokhba International Trading website completely.

## 📦 محتويات الأرشيف / Archive Contents

### 🔧 الكود المصدري / Source Code
```
nokhba_website/nokhba_trade_flask/
├── src/
│   ├── main.py                 # التطبيق الرئيسي Flask / Main Flask application
│   ├── templates/              # قوالب HTML / HTML templates
│   │   ├── base.html          # القالب الأساسي / Base template
│   │   ├── index.html         # الصفحة الرئيسية / Homepage
│   │   ├── trading_services.html  # صفحة خدمات التجارة / Trading services page
│   │   ├── import_export.html     # صفحة الاستيراد والتصدير / Import/Export page
│   │   └── contact.html           # صفحة التواصل / Contact page
│   └── static/
│       └── images/            # جميع صور الموقع / All website images
├── requirements.txt           # متطلبات Python / Python requirements
└── templates/                # قوالب إضافية / Additional templates
```

### 🖼️ الصور والأصول / Images and Assets
```
nokhba_website/nokhba_trade_flask/src/static/images/
├── modern_office.jpg          # مكتب حديث / Modern office
├── business_handshake.jpg     # مصافحة أعمال / Business handshake
├── shipping_containers.jpg    # حاويات الشحن / Shipping containers
├── technology_office.jpg      # مكتب تقني / Technology office
├── warehouse_storage.jpg      # مستودع التخزين / Warehouse storage
├── data_center.jpg           # مركز البيانات / Data center
├── networking_conference.jpg  # مؤتمر الشبكات / Networking conference
├── shipping_port.jpg         # ميناء الشحن / Shipping port
├── innovation_lab.jpg        # مختبر الابتكار / Innovation lab
├── global_shipping.jpg       # الشحن العالمي / Global shipping
└── [المزيد من الصور / More images...]
```

### 📄 الوثائق والمحتوى / Documentation and Content
```
nokhba_website/
├── website_structure.md      # هيكل الموقع / Website structure
├── content.md               # المحتوى الأساسي / Basic content
├── detailed_content.md      # المحتوى المفصل / Detailed content
└── assets/
    └── logos/              # شعارات الشركاء / Partner logos
        ├── dell_logo.png
        ├── hp_logo.jpg
        ├── hikvision_logo.png
        ├── benq_logo.png
        ├── lenovo_logo.png
        ├── samsung_logo.png
        └── asus_logo.png
```

### ⚙️ ملفات الإعداد / Setup Files
```
├── README_NOKHBA_WEBSITE.md   # دليل المشروع الرئيسي / Main project guide
├── setup_website.sh          # سكريبت إعداد Linux/Mac / Linux/Mac setup script
├── setup_website.bat         # سكريبت إعداد Windows / Windows setup script
└── project_files_list.txt    # قائمة ملفات المشروع / Project files list
```

## 🚀 طريقة إعادة البناء / Rebuild Instructions

### 1️⃣ استخراج الملفات / Extract Files
```bash
tar -xzf nokhba_website_complete_source.tar.gz
cd nokhba_website/
```

### 2️⃣ إعداد البيئة / Environment Setup
```bash
# إنشاء بيئة افتراضية / Create virtual environment
python3 -m venv venv

# تفعيل البيئة / Activate environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# تثبيت المتطلبات / Install requirements
cd nokhba_trade_flask/
pip install -r requirements.txt
```

### 3️⃣ تشغيل الموقع / Run Website
```bash
cd src/
python main.py
```

### 4️⃣ الوصول للموقع / Access Website
افتح المتصفح وانتقل إلى / Open browser and go to: `http://localhost:5000`

## 🔧 التعديل والتطوير / Modification and Development

### تعديل المحتوى / Content Modification
- **النصوص**: عدّل ملفات HTML في مجلد `templates/`
- **الصور**: استبدل الصور في مجلد `static/images/`
- **التصميم**: عدّل CSS في ملفات HTML

### إضافة صفحات جديدة / Adding New Pages
1. أنشئ ملف HTML جديد في `templates/`
2. أضف مسار جديد في `main.py`
3. حدّث القائمة في `base.html`

### تحديث الوظائف / Function Updates
- **محول العملات**: عدّل في `main.py`
- **نموذج الاتصال**: عدّل في `contact.html` و `main.py`
- **خريطة Google**: عدّل في `contact.html`

## 📊 الوظائف المتاحة / Available Features

### 💱 محول العملات / Currency Converter
- **API Endpoint**: `/api/exchange-rates`
- **العملات المدعومة**: USD, EGP, AED, EUR, CNY, TRY
- **مصدر الأسعار**: exchangerate-api.com

### 🗺️ خريطة تفاعلية / Interactive Map
- **Google Maps** مدمجة في صفحة التواصل
- **الموقع**: القاهرة، مصر
- **التفاعل**: تكبير، تصغير، اتجاهات

### 📱 تصميم متجاوب / Responsive Design
- **متوافق مع الجوال** / Mobile compatible
- **تصميم مرن** / Flexible design
- **دعم جميع الأجهزة** / All devices support

## 🎨 التخصيص / Customization

### الألوان / Colors
```css
الأزرق الأساسي / Primary Blue: #1e40af
البرتقالي المميز / Accent Orange: #f97316
الرمادي الفاتح / Light Gray: #f8f9fa
الأبيض / White: #ffffff
```

### الخطوط / Fonts
- **العربية**: Arial, sans-serif
- **الإنجليزية**: Arial, sans-serif
- **أحجام متدرجة** / Graduated sizes

### الصور / Images
- **دقة عالية** / High resolution
- **تحسين للويب** / Web optimized
- **أحجام متوسطة** / Medium sizes
- **تنسيقات**: JPG, PNG, WebP

## 🔒 الأمان / Security

### متطلبات الأمان / Security Requirements
- **CORS** مُفعّل للتطبيقات المتقدمة
- **تشفير HTTPS** موصى به للإنتاج
- **تحديث المكتبات** بانتظام

### النسخ الاحتياطية / Backups
- **نسخ دورية** للملفات المصدرية
- **حفظ قاعدة البيانات** (إذا أُضيفت لاحقاً)
- **أرشفة الصور** والأصول

## 📈 التطوير المستقبلي / Future Development

### إضافات مقترحة / Suggested Additions
- **قاعدة بيانات** لإدارة المنتجات
- **لوحة تحكم إدارية** / Admin panel
- **نظام إدارة المحتوى** / CMS
- **تحليلات الموقع** / Website analytics

### التحسينات / Improvements
- **تحسين SEO** / SEO optimization
- **ضغط الصور** / Image compression
- **تسريع التحميل** / Loading speed
- **دعم لغات متعددة** / Multi-language support

## 🛠️ استكشاف الأخطاء / Troubleshooting

### مشاكل شائعة / Common Issues
1. **خطأ في تثبيت المتطلبات**: تأكد من إصدار Python 3.8+
2. **عدم ظهور الصور**: تحقق من مسارات الملفات
3. **خطأ في محول العملات**: تحقق من الاتصال بالإنترنت

### الحلول / Solutions
- **إعادة تثبيت المتطلبات**: `pip install -r requirements.txt --force-reinstall`
- **تحديث المسارات**: تأكد من المسارات النسبية
- **فحص السجلات**: راجع رسائل الخطأ في Terminal

## 📞 الدعم / Support

### معلومات الاتصال / Contact Information
- **الشركة**: النخبة للتجارة الدولية
- **الهاتف**: +20 12 22233255
- **البريد الإلكتروني**: mosaad@nokhbatrade.com

### الموارد / Resources
- **Flask Documentation**: https://flask.palletsprojects.com/
- **Python Documentation**: https://docs.python.org/
- **HTML/CSS Guides**: https://developer.mozilla.org/

## 📝 الترخيص / License

هذا المشروع مطور خصيصاً لشركة النخبة للتجارة الدولية.
جميع الحقوق محفوظة © 2025

This project is developed specifically for Al-Nokhba International Trading.
All rights reserved © 2025

---

**ملاحظة**: هذا الأرشيف يحتوي على كل ما تحتاجه لإعادة بناء الموقع بالكامل والتعديل عليه.

**Note**: This archive contains everything you need to completely rebuild and modify the website.

