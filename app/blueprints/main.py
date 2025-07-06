"""
Main Blueprint for Al-Nokhba International Trading Website
Contains all main website routes
"""

from flask import Blueprint, render_template, request, jsonify

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Homepage route"""
    return render_template('index.html')


@main_bp.route('/trading-services')
def trading_services():
    """Trading Services page route"""
    return render_template('trading_services.html')


@main_bp.route('/import-export')
def import_export():
    """Import & Export page route"""
    return render_template('import_export.html')


@main_bp.route('/contact')
def contact():
    """Contact page route"""
    return render_template('contact.html')


@main_bp.route('/contact', methods=['POST'])
def contact_form():
    """Handle contact form submission"""
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        # Here you would typically save to database or send email
        # For now, we'll just return a success response
        
        return jsonify({
            'success': True,
            'message': 'تم إرسال رسالتك بنجاح. سنتواصل معك قريباً.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'حدث خطأ في إرسال الرسالة. يرجى المحاولة مرة أخرى.'
        }), 500


@main_bp.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@main_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500

