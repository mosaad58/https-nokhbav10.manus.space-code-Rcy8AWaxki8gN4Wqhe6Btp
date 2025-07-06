"""
Al-Nokhba International Trading Website
Main application entry point for Railway deployment
"""

import os
from app import create_app

# Create Flask application
app = create_app()

if __name__ == '__main__':
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get('PORT', 5000))
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    )

