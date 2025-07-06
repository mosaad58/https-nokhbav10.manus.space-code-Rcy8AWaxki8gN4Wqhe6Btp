# Al-Nokhba International Trading Website

A professional Flask web application for Al-Nokhba International Trading Company, built with modern web technologies and optimized for Railway deployment.

## 🚀 Railway Deployment

This application is specifically configured for deployment on Railway with the following features:

- **Flask Application Factory Pattern** with Blueprints
- **Gunicorn WSGI Server** for production
- **Health Check Endpoint** for Railway monitoring
- **Environment Variable Configuration**
- **Static File Serving** optimized for production

## 📁 Project Structure

```
nokhba_railway_app/
├── app/
│   ├── __init__.py              # Flask application factory
│   ├── blueprints/
│   │   ├── __init__.py
│   │   ├── main.py              # Main website routes
│   │   └── api.py               # API endpoints (currency converter)
│   ├── static/
│   │   ├── images/              # All website images and logos
│   │   ├── css/                 # CSS files (if separated)
│   │   └── js/                  # JavaScript files (if separated)
│   └── templates/               # Jinja2 HTML templates
│       ├── base.html            # Base template
│       ├── index.html           # Homepage
│       ├── trading_services.html
│       ├── import_export.html
│       ├── contact.html
│       ├── 404.html             # Error pages
│       └── 500.html
├── config/                      # Configuration files
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── Procfile                     # Railway process configuration
├── railway.json                 # Railway deployment configuration
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## 🛠️ Features

### 💱 Currency Converter
- Real-time exchange rates from multiple APIs
- Support for 20+ currencies including Middle Eastern currencies
- Fallback to default rates if APIs are unavailable
- RESTful API endpoint: `/api/exchange-rates`

### 🌐 Multi-language Support
- Arabic and English content
- RTL (Right-to-Left) text support
- Localized number formatting

### 📱 Responsive Design
- Mobile-first approach
- Bootstrap-based responsive grid
- Touch-friendly interface
- Cross-browser compatibility

### 🗺️ Interactive Features
- Google Maps integration
- Contact form with validation
- Dynamic content loading
- SEO-optimized structure

## 🚀 Deployment on Railway

### 1. Quick Deploy
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

### 2. Manual Deployment

1. **Fork/Clone this repository**
2. **Connect to Railway:**
   - Go to [Railway](https://railway.app)
   - Create new project from GitHub repo
   - Select this repository

3. **Environment Variables (Optional):**
   ```
   FLASK_DEBUG=False
   SECRET_KEY=your-secret-key-here
   ```

4. **Deploy:**
   - Railway will automatically detect the Flask app
   - Build and deploy using the Procfile configuration
   - Access your app at the provided Railway URL

### 3. Local Development

```bash
# Clone the repository
git clone <repository-url>
cd nokhba_railway_app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (optional)
cp .env.example .env
# Edit .env with your values

# Run the application
python main.py
```

## 📡 API Endpoints

### Currency Converter
```
GET /api/exchange-rates?from=USD&to=EGP&amount=100
```

**Response:**
```json
{
  "from": "USD",
  "to": "EGP",
  "rate": 49.35,
  "amount": 100,
  "converted_amount": 4935.00,
  "timestamp": "2025-01-01T12:00:00Z"
}
```

### Health Check
```
GET /api/health
```

### Supported Currencies
```
GET /api/currencies
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port (set by Railway) | `5000` |
| `FLASK_DEBUG` | Enable debug mode | `False` |
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |

### Railway Configuration

The `railway.json` file contains Railway-specific configuration:
- Build settings
- Health check configuration
- Restart policy
- Start command

## 🏗️ Architecture

### Flask Application Factory
The application uses the Flask Application Factory pattern with blueprints for better organization:

- **Main Blueprint** (`app/blueprints/main.py`): Website routes
- **API Blueprint** (`app/blueprints/api.py`): API endpoints

### Database (Future Enhancement)
Currently, the application is stateless. For future enhancements, you can add:
- PostgreSQL database (Railway provides this)
- SQLAlchemy ORM
- User authentication
- Content management

## 🎨 Customization

### Adding New Pages
1. Create HTML template in `app/templates/`
2. Add route in `app/blueprints/main.py`
3. Update navigation in `base.html`

### Styling
- CSS is embedded in HTML templates
- For larger projects, extract to `app/static/css/`
- Update static file references in templates

### Adding New API Endpoints
1. Add routes to `app/blueprints/api.py`
2. Follow RESTful conventions
3. Include proper error handling

## 🔒 Security

- CORS enabled for API endpoints
- Environment variable configuration
- Input validation on forms
- Error handling without information disclosure

## 📊 Monitoring

- Health check endpoint: `/api/health`
- Railway provides built-in monitoring
- Logs available in Railway dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For support and inquiries:
- **Company**: Al-Nokhba International Trading
- **Phone**: +20 12 22233255
- **Email**: mosaad@nokhbatrade.com

## 📄 License

This project is proprietary software developed for Al-Nokhba International Trading Company.
All rights reserved © 2025

---

**Built with ❤️ for Al-Nokhba International Trading**

