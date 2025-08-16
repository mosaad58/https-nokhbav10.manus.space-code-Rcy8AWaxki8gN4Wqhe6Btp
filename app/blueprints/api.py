"""
API Blueprint for Al-Nokhba International Trading Website
Contains all API endpoints including currency converter with improved error handling
"""

from flask import Blueprint, request, jsonify
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
import time

api_bp = Blueprint('api', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a session with retry strategy
def create_requests_session():
    """Create a requests session with retry strategy and proper headers"""
    session = requests.Session()
    
    # Define retry strategy
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"],
        backoff_factor=1
    )
    
    # Mount adapter with retry strategy
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Set headers to mimic a real browser
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    return session

# Global session instance
http_session = create_requests_session()


def get_exchange_rate_from_api(from_currency, to_currency):
    """Get exchange rate from external API with better error handling"""
    try:
        # Try multiple APIs in sequence
        apis_to_try = [
            {
                'name': 'exchangerate-api',
                'url': f"https://api.exchangerate-api.com/v4/latest/{from_currency}",
                'parser': lambda data: data.get('rates', {}).get(to_currency)
            },
            {
                'name': 'freeforexapi',
                'url': f"https://api.freeforexapi.com/api/live?pairs={from_currency}{to_currency}",
                'parser': lambda data: data.get('rates', {}).get(f"{from_currency}{to_currency}", {}).get('rate')
            },
            {
                'name': 'currencyapi',
                'url': f"https://api.currencyapi.com/v3/latest?apikey=YOUR_API_KEY&currencies={to_currency}&base_currency={from_currency}",
                'parser': lambda data: data.get('data', {}).get(to_currency, {}).get('value')
            }
        ]
        
        for api in apis_to_try:
            try:
                logger.info(f"Trying {api['name']} API...")
                
                # Make request with timeout and session
                response = http_session.get(
                    api['url'], 
                    timeout=(5, 10),  # (connection timeout, read timeout)
                    allow_redirects=True
                )
                
                if response.status_code == 200:
                    data = response.json()
                    rate = api['parser'](data)
                    
                    if rate and isinstance(rate, (int, float)) and rate > 0:
                        logger.info(f"Successfully got rate from {api['name']}: {rate}")
                        return float(rate)
                else:
                    logger.warning(f"{api['name']} returned status code: {response.status_code}")
                    
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"Connection error with {api['name']}: {e}")
                continue
            except requests.exceptions.Timeout as e:
                logger.warning(f"Timeout error with {api['name']}: {e}")
                continue
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request error with {api['name']}: {e}")
                continue
            except (KeyError, ValueError, TypeError) as e:
                logger.warning(f"Data parsing error with {api['name']}: {e}")
                continue
            
            # Small delay between API attempts
            time.sleep(0.5)
                
    except Exception as e:
        logger.error(f"Unexpected error fetching exchange rate: {e}")
    
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
        'USD_LYD': 4.85,
        # Add reverse rates
        'EGP_USD': 1/49.35,
        'AED_USD': 1/3.67,
        'EUR_USD': 1/0.848,
        'CNY_USD': 1/7.16,
        'TRY_USD': 1/39.89,
        'SAR_USD': 1/3.75,
        # Add cross rates (example)
        'EUR_EGP': 49.35 * 0.848,
        'AED_EGP': 49.35 / 3.67,
    }
    
    # If direct pair not found, try reverse
    if currency_pair not in default_rates:
        from_curr, to_curr = currency_pair.split('_')
        reverse_pair = f"{to_curr}_{from_curr}"
        if reverse_pair in default_rates:
            return 1 / default_rates[reverse_pair]
    
    return default_rates.get(currency_pair, 1.0)


def safe_get_timestamp():
    """Safely get timestamp without external API dependency"""
    try:
        response = http_session.get('http://worldtimeapi.org/api/timezone/UTC', timeout=3)
        if response.status_code == 200:
            return response.json().get('datetime', time.strftime('%Y-%m-%dT%H:%M:%SZ'))
    except:
        pass
    
    # Fallback to local time
    return time.strftime('%Y-%m-%dT%H:%M:%SZ')


@api_bp.route('/exchange-rates')
def exchange_rates():
    """Currency exchange rates API endpoint with improved error handling"""
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
            source = 'direct'
        else:
            # Try to get rate from API
            rate = get_exchange_rate_from_api(from_currency, to_currency)
            
            # If API fails, use default rates
            if rate is None:
                currency_pair = f"{from_currency}_{to_currency}"
                rate = get_default_rate(currency_pair)
                source = 'fallback'
                logger.warning(f"Using default rate for {currency_pair}: {rate}")
            else:
                source = 'live'
        
        # Calculate converted amount
        converted_amount = amount * rate
        
        return jsonify({
            'from': from_currency,
            'to': to_currency,
            'rate': round(rate, 6),
            'amount': amount,
            'converted_amount': round(converted_amount, 2),
            'source': source,  # Indicates if rate is 'live', 'fallback', or 'direct'
            'timestamp': safe_get_timestamp(),
            'status': 'success'
        })
        
    except ValueError:
        return jsonify({
            'error': 'Invalid amount parameter',
            'status': 'error'
        }), 400
    except Exception as e:
        logger.error(f"Exchange rate API error: {e}")
        return jsonify({
            'error': 'Internal server error',
            'status': 'error'
        }), 500


@api_bp.route('/health')
def health_check():
    """Health check endpoint for Railway"""
    return jsonify({
        'status': 'healthy',
        'service': 'Al-Nokhba International Trading Website',
        'version': '1.0.0',
        'timestamp': safe_get_timestamp()
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
    
    return jsonify({
        'currencies': currencies,
        'count': len(currencies),
        'status': 'success'
    })


@api_bp.route('/test-connection')
def test_connection():
    """Test external API connections"""
    test_results = {}
    
    try:
        # Test exchangerate-api
        response = http_session.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=5)
        test_results['exchangerate-api'] = {
            'status': 'success' if response.status_code == 200 else 'failed',
            'status_code': response.status_code,
            'response_time': response.elapsed.total_seconds()
        }
    except Exception as e:
        test_results['exchangerate-api'] = {
            'status': 'error',
            'error': str(e)
        }
    
    return jsonify({
        'test_results': test_results,
        'timestamp': safe_get_timestamp()
    })
