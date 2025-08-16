"""
API Blueprint for Al-Nokhba International Trading Website
Contains all API endpoints including currency converter with enhanced error handling
"""

from flask import Blueprint, request, jsonify
import requests
import logging
import time
from functools import wraps

api_bp = Blueprint('api', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retry_on_failure(max_retries=3, delay=1):
    """Decorator to retry API calls on failure"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.error(f"Final attempt failed for {func.__name__}: {e}")
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {delay}s...")
                    time.sleep(delay * (attempt + 1))  # Exponential backoff
            return None
        return wrapper
    return decorator

@retry_on_failure(max_retries=2, delay=2)
def get_exchange_rate_from_api(from_currency, to_currency):
    """Get exchange rate from external API with improved error handling"""
    try:
        # Primary API: exchangerate-api.com (Open Access - no key required)
        # Using the open access endpoint which is more reliable for free usage
        url = f"https://open.er-api.com/v6/latest/{from_currency}"
        
        headers = {
            'User-Agent': 'Al-Nokhba-Trading-App/1.0',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, timeout=15, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('result') == 'success' and 'rates' in data:
                if to_currency in data['rates']:
                    logger.info(f"Successfully fetched rate from primary API: {from_currency} to {to_currency}")
                    return data['rates'][to_currency]
        elif response.status_code == 429:
            logger.warning("Rate limit hit on primary API")
            raise requests.exceptions.RequestException("Rate limit exceeded")
        
        # Secondary API: Alternative free service
        # Using a different free API as backup
        backup_url = f"https://api.fxratesapi.com/latest?base={from_currency}&currencies={to_currency}"
        backup_response = requests.get(backup_url, timeout=15, headers=headers)
        
        if backup_response.status_code == 200:
            backup_data = backup_response.json()
            if 'rates' in backup_data and to_currency in backup_data['rates']:
                logger.info(f"Successfully fetched rate from backup API: {from_currency} to {to_currency}")
                return backup_data['rates'][to_currency]
                
    except requests.exceptions.Timeout:
        logger.error("API request timed out")
        raise
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching exchange rate: {e}")
        raise
    
    return None

def get_default_rate(currency_pair):
    """Get default exchange rates as fallback with updated 2025 rates"""
    # Updated rates as of August 2025
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
        'USD_LYD': 4.85,
        # Add reverse rates for common conversions
        'EGP_USD': 1/49.35,
        'AED_USD': 1/3.67,
        'EUR_USD': 1/0.848,
        'CNY_USD': 1/7.16,
        'TRY_USD': 1/39.89,
        'SAR_USD': 1/3.75,
    }
    
    # Try direct lookup first
    rate = default_rates.get(currency_pair)
    if rate:
        return rate
    
    # Try reverse lookup
    reverse_pair = f"{currency_pair.split('_')[1]}_{currency_pair.split('_')[0]}"
    reverse_rate = default_rates.get(reverse_pair)
    if reverse_rate:
        return 1 / reverse_rate
    
    # Default fallback
    return 1.0

@api_bp.route('/exchange-rates')
def exchange_rates():
    """Currency exchange rates API endpoint with enhanced error handling"""
    try:
        from_currency = request.args.get('from', 'USD').upper()
        to_currency = request.args.get('to', 'EGP').upper()
        amount = float(request.args.get('amount', 1))
        
        # Validate currencies
        supported_currencies = [
            'USD', 'EGP', 'AED', 'EUR', 'CNY', 'TRY', 'SAR', 'KWD', 
            'QAR', 'BHD', 'OMR', 'JOD', 'LBP', 'IQD', 'SYP', 'YER', 
            'MAD', 'TND', 'DZD', 'LYD', 'GBP', 'JPY', 'CAD', 'AUD'
        ]
        
        if from_currency not in supported_currencies or to_currency not in supported_currencies:
            return jsonify({
                'error': 'Unsupported currency',
                'supported_currencies': supported_currencies
            }), 400
        
        # If same currency, return 1
        if from_currency == to_currency:
            rate = 1.0
            source = 'direct'
        else:
            rate = None
            source = 'default'
            
            # Try to get rate from API with error handling
            try:
                rate = get_exchange_rate_from_api(from_currency, to_currency)
                if rate:
                    source = 'api'
            except Exception as e:
                logger.warning(f"API call failed, using default rates: {e}")
            
            # If API fails, use default rates
            if rate is None:
                currency_pair = f"{from_currency}_{to_currency}"
                rate = get_default_rate(currency_pair)
                logger.info(f"Using default rate for {currency_pair}: {rate}")
        
        # Calculate converted amount
        converted_amount = amount * rate
        
        # Get current timestamp safely
        try:
            timestamp_response = requests.get('http://worldtimeapi.org/api/timezone/UTC', timeout=5)
            timestamp = timestamp_response.json().get('datetime', 'N/A') if timestamp_response.status_code == 200 else 'N/A'
        except:
            timestamp = 'N/A'
        
        return jsonify({
            'from': from_currency,
            'to': to_currency,
            'rate': rate,
            'amount': amount,
            'converted_amount': round(converted_amount, 2),
            'source': source,
            'timestamp': timestamp,
            'status': 'success'
        })
        
    except ValueError:
        return jsonify({'error': 'Invalid amount parameter', 'status': 'error'}), 400
    except Exception as e:
        logger.error(f"Exchange rate API error: {e}")
        return jsonify({
            'error': 'Internal server error', 
            'status': 'error',
            'message': 'Please try again later'
        }), 500

@api_bp.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'service': 'Al-Nokhba International Trading Website',
        'version': '1.0.0',
        'timestamp': time.time()
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
        'LYD': 'Libyan Dinar',
        'GBP': 'British Pound',
        'JPY': 'Japanese Yen',
        'CAD': 'Canadian Dollar',
        'AUD': 'Australian Dollar'
    }
    
    return jsonify({
        'currencies': currencies,
        'count': len(currencies),
        'status': 'success'
    })

