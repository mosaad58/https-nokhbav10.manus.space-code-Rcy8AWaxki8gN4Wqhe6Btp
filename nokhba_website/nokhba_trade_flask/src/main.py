from flask import Flask, render_template, request, jsonify
import os
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__, static_folder='static', template_folder='templates')

# إنشاء مجلد templates إذا لم يكن موجوداً
os.makedirs('templates', exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trading-services')
def trading_services():
    return render_template('trading_services.html')

@app.route('/import-export')
def import_export():
    return render_template('import_export.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        # هنا يمكن إضافة منطق حفظ البيانات أو إرسال إيميل
        return jsonify({'status': 'success', 'message': 'تم إرسال رسالتك بنجاح. سنتواصل معك قريباً.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'حدث خطأ في إرسال الرسالة. يرجى المحاولة مرة أخرى.'})

@app.route('/api/exchange-rates')
def get_exchange_rates():
    try:
        # قائمة العملات المطلوبة
        currencies = {
            'EGP': 'Egyptian Pound',
            'AED': 'UAE Dirham', 
            'TRY': 'Turkish Lira',
            'CNY': 'Chinese Yuan',
            'EUR': 'Euro'
        }
        
        rates = {}
        
        # محاولة الحصول على الأسعار من exchangerate-api.com (مجاني ودقيق)
        try:
            api_url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                api_rates = data.get('rates', {})
                
                for currency_code, currency_name in currencies.items():
                    if currency_code in api_rates:
                        rates[currency_code] = {
                            'rate': round(api_rates[currency_code], 4),
                            'name': currency_name,
                            'symbol': get_currency_symbol(currency_code)
                        }
                
                # إذا حصلنا على جميع الأسعار من API، نعيدها
                if len(rates) == len(currencies):
                    return jsonify({'status': 'success', 'rates': rates})
        except:
            pass
        
        # إذا فشل API، نحاول الحصول على الأسعار من Oanda
        for currency_code, currency_name in currencies.items():
            if currency_code not in rates:
                try:
                    rate = get_oanda_rate('USD', currency_code)
                    if rate:
                        rates[currency_code] = {
                            'rate': rate,
                            'name': currency_name,
                            'symbol': get_currency_symbol(currency_code)
                        }
                    else:
                        rates[currency_code] = {
                            'rate': get_default_rate(currency_code),
                            'name': currency_name,
                            'symbol': get_currency_symbol(currency_code)
                        }
                except:
                    rates[currency_code] = {
                        'rate': get_default_rate(currency_code),
                        'name': currency_name,
                        'symbol': get_currency_symbol(currency_code)
                    }
        
        return jsonify({'status': 'success', 'rates': rates})
        
    except Exception as e:
        # في حالة فشل كل شيء، استخدم الأسعار الافتراضية
        rates = {}
        currencies = {
            'EGP': 'Egyptian Pound',
            'AED': 'UAE Dirham', 
            'TRY': 'Turkish Lira',
            'CNY': 'Chinese Yuan',
            'EUR': 'Euro'
        }
        
        for currency_code, currency_name in currencies.items():
            rates[currency_code] = {
                'rate': get_default_rate(currency_code),
                'name': currency_name,
                'symbol': get_currency_symbol(currency_code)
            }
        
        return jsonify({'status': 'success', 'rates': rates})

def get_oanda_rate(from_currency, to_currency):
    try:
        url = f"https://www.oanda.com/currency-converter/en/?from={from_currency}&to={to_currency}&amount=1"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # البحث عن عنصر النتيجة بطرق مختلفة
            rate_selectors = [
                'input[data-testid="conversion-result-input"]',
                'input[data-module="CurrencyConverter"]',
                '.result-input input',
                'input[readonly]'
            ]
            
            for selector in rate_selectors:
                rate_element = soup.select_one(selector)
                if rate_element and rate_element.get('value'):
                    try:
                        rate_value = rate_element.get('value').replace(',', '')
                        rate = float(rate_value)
                        return round(rate, 4)
                    except:
                        continue
            
            # البحث في النص
            text_content = soup.get_text()
            # البحث عن نمط الأرقام في النص
            import re
            patterns = [
                rf'{to_currency}.*?(\d+\.?\d*)',
                rf'(\d+\.?\d*).*?{to_currency}',
                r'(\d{1,3}(?:,\d{3})*(?:\.\d{2,4})?)'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, text_content)
                for match in matches:
                    try:
                        rate = float(match.replace(',', ''))
                        if 0.01 <= rate <= 10000:  # نطاق معقول للأسعار
                            return round(rate, 4)
                    except:
                        continue
                        
    except Exception as e:
        print(f"Error getting rate from Oanda: {e}")
    
    return None

def get_currency_symbol(currency_code):
    symbols = {
        'EGP': 'ج.م',
        'AED': 'د.إ',
        'TRY': '₺',
        'CNY': '¥',
        'EUR': '€'
    }
    return symbols.get(currency_code, currency_code)

def get_default_rate(currency_code):
    # أسعار افتراضية محدثة (يوليو 2025) - من exchangerate-api.com
    default_rates = {
        'EGP': 49.35,   # الجنيه المصري
        'AED': 3.67,    # الدرهم الإماراتي
        'TRY': 39.89,   # الليرة التركية
        'CNY': 7.16,    # اليوان الصيني
        'EUR': 0.848    # اليورو
    }
    return default_rates.get(currency_code, 1.0)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

