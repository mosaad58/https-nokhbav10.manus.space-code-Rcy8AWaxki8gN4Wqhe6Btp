"""
API Blueprint for Al-Nokhba International Trading Website
Contains all API endpoints including currency converter
"""

from flask import Blueprint, request, jsonify
import requests
import logging

api_bp = Blueprint('api', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_exchange_rate_from_api(from_currency, to_currency):
    try:
        url = f"https://api.frankfurter.app/latest?from={from_currency}&to={to_currency}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'rates' in data and to_currency in data['rates']:
                return data['rates'][to_currency]
    except Exception as e:
        logger.error(f"Error fetching exchange rate: {e}")
    return None


def get_default_rate(currency_pair):
    """Get default exchange rates as fallback"""
    # Updated rates as of 2025 (more current)
    default_rates = {
        'USD_EGP': 49.35,
        'USD_AED': 3.67,
        'USD_EUR': 0.848,
        'USD_CNY': 7.16,
        'USD_TRY': 39.89,
        'USD_SAR': 3.75,
        'USD_KWD': 0.307,
        'USD_QAR': 3.64,
        'USD_BHD': 0.376,
        'USD_OMR': 0.385,
        'USD_JOD': 0.709,
        'USD_LBP': 89500,
        'USD_IQD': 1310,
        'USD_SYP': 13000,
        'USD_YER': 250,
        'USD_MAD': 9.85,
        'USD_TND': 3.12,
        'USD_DZD': 134.5,
        'USD_LYD': 4.85
    }
    
    return default_rates.get(currency_pair, 1.0)


@api_bp.route('/exchange-rates')
def exchange_rates():
    """Currency exchange rates API endpoint"""
    try:
        from_currency = request.args.get('from', 'USD').upper()
        to_currency = request.args.get('to', 'EGP').upper()
        amount = float(request.args.get('amount', 1))
        
        # Validate currencies
        supported_currencies = ['USD', 'EGP', 'AED', 'EUR', 'CNY', 'TRY', 'SAR', 'KWD', 'QAR', 'BHD', 'OMR', 'JOD', 'LBP', 'IQD', 'SYP', 'YER', 'MAD', 'TND', 'DZD', 'LYD']
        
        if from_currency not in supported_currencies or to_currency not in supported_currencies:
            return jsonify({
                'error': 'Unsupported currency',
                'supported_currencies': supported_currencies
            }), 400
        
        # If same currency, return 1
        if from_currency == to_currency:
            rate = 1.0
        else:
            # Try to get rate from API
            rate = get_exchange_rate_from_api(from_currency, to_currency)
            
            # If API fails, use default rates
            if rate is None:
                currency_pair = f"{from_currency}_{to_currency}"
                rate = get_default_rate(currency_pair)
                logger.warning(f"Using default rate for {currency_pair}: {rate}")
        
        # Calculate converted amount
        converted_amount = amount * rate
        
        return jsonify({
            'from': from_currency,
            'to': to_currency,
            'rate': rate,
            'amount': amount,
            'converted_amount': round(converted_amount, 2),
            'timestamp': requests.get('http://worldtimeapi.org/api/timezone/UTC').json().get('datetime', 'N/A') if requests else 'N/A'
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid amount parameter'}), 400
    except Exception as e:
        logger.error(f"Exchange rate API error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@api_bp.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'service': 'Al-Nokhba International Trading Website',
        'version': '1.0.0'
    })


@api_bp.route('/currencies')
def supported_currencies():
    """Get list of supported currencies"""
    currencies = {
        'USD': 'US Dollar',
        'EGP': 'Egyptian Pound',
        'AED': 'UAE Dirham',
        'EUR': 'Euro',
        'CNY': 'Chinese Yuan',
        'TRY': 'Turkish Lira',
        'SAR': 'Saudi Riyal',
        'KWD': 'Kuwaiti Dinar',
        'QAR': 'Qatari Riyal',
        'BHD': 'Bahraini Dinar',
        'OMR': 'Omani Rial',
        'JOD': 'Jordanian Dinar',
        'LBP': 'Lebanese Pound',
        'IQD': 'Iraqi Dinar',
        'SYP': 'Syrian Pound',
        'YER': 'Yemeni Rial',
        'MAD': 'Moroccan Dirham',
        'TND': 'Tunisian Dinar',
        'DZD': 'Algerian Dinar',
        'LYD': 'Libyan Dinar'
    }
    
    return jsonify(currencies)
