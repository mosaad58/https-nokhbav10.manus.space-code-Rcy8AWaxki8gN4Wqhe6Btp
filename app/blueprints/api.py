// Alternative Frontend JavaScript Solution (Approach 2)
// Replace the existing JavaScript in your index.html {% block extra_js %} section

// Currency Converter functionality
let exchangeRates = {};
let lastUpdateTime = null;

// Currency configurations
const targetCurrencies = [
    { code: 'EGP', name: 'Egyptian Pound', symbol: 'ج.م', flag: '🇪🇬' },
    { code: 'AED', name: 'UAE Dirham', symbol: 'د.إ', flag: '🇦🇪' },
    { code: 'TRY', name: 'Turkish Lira', symbol: '₺', flag: '🇹🇷' },
    { code: 'CNY', name: 'Chinese Yuan', symbol: '¥', flag: '🇨🇳' },
    { code: 'EUR', name: 'Euro', symbol: '€', flag: '🇪🇺' }
];

// Load exchange rates for multiple currencies
async function loadExchangeRates() {
    const resultsContainer = document.getElementById('currencyResults');
    resultsContainer.innerHTML = '<div class="loading">Loading exchange rates...</div>';
    
    try {
        const rates = {};
        
        // Fetch rates for each target currency
        for (const currency of targetCurrencies) {
            try {
                const response = await fetch(`/api/exchange-rates?from=USD&to=${currency.code}&amount=1`);
                const data = await response.json();
                
                if (data.status === 'success') {
                    rates[currency.code] = {
                        name: currency.name,
                        symbol: currency.symbol,
                        rate: data.rate,
                        source: data.source
                    };
                } else {
                    throw new Error(`Failed to get rate for ${currency.code}: ${data.error || 'Unknown error'}`);
                }
            } catch (error) {
                console.error(`Error fetching ${currency.code} rate:`, error);
                // Provide fallback rate
                rates[currency.code] = {
                    name: currency.name,
                    symbol: currency.symbol,
                    rate: getDefaultRate('USD', currency.code),
                    source: 'default'
                };
            }
        }
        
        // Check if we got any rates
        if (Object.keys(rates).length === 0) {
            throw new Error('No exchange rates could be loaded');
        }
        
        exchangeRates = rates;
        lastUpdateTime = new Date();
        displayCurrencyResults();
        updateLastUpdatedTime();
        
    } catch (error) {
        console.error('Error loading exchange rates:', error);
        showError('Unable to load current exchange rates. Please try again later.');
    }
}

// Fallback rates function
function getDefaultRate(from, to) {
    const defaultRates = {
        'USD_EGP': 49.35,
        'USD_AED': 3.67,
        'USD_EUR': 0.848,
        'USD_CNY': 7.16,
        'USD_TRY': 39.89
    };
    return defaultRates[`${from}_${to}`] || 1.0;
}

// Display currency conversion results
function displayCurrencyResults() {
    const resultsContainer = document.getElementById('currencyResults');
    const usdAmount = parseFloat(document.getElementById('usdAmount').value) || 1;
    
    if (Object.keys(exchangeRates).length === 0) {
        showError('No exchange rates available');
        return;
    }
    
    let html = '<div class="currency-grid">';
    
    for (const currency of targetCurrencies) {
        const rateData = exchangeRates[currency.code];
        if (rateData) {
            const convertedAmount = (usdAmount * rateData.rate).toFixed(2);
            
            html += `
                <div class="currency-item">
                    <div class="currency-flag">${currency.flag}</div>
                    <div class="currency-name">${rateData.name}</div>
                    <div class="currency-code">${currency.code}</div>
                    <div class="currency-value">${convertedAmount}</div>
                    <div class="currency-symbol">${rateData.symbol}</div>
                </div>
            `;
        }
    }
    
    html += '</div>';
    resultsContainer.innerHTML = html;
}

// Show error message
function showError(message) {
    const resultsContainer = document.getElementById('currencyResults');
    resultsContainer.innerHTML = `<div class="error">${message}</div>`;
}

// Update last updated time
function updateLastUpdatedTime() {
    if (lastUpdateTime) {
        const timeString = lastUpdateTime.toLocaleString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        document.getElementById('lastUpdated').textContent = `Last updated: ${timeString}`;
    }
}

// Initialize currency converter
document.addEventListener('DOMContentLoaded', function() {
    // Load exchange rates on page load
    loadExchangeRates();
    
    // Update conversion when amount changes
    const usdAmountInput = document.getElementById('usdAmount');
    if (usdAmountInput) {
        usdAmountInput.addEventListener('input', function() {
            if (Object.keys(exchangeRates).length > 0) {
                displayCurrencyResults();
            }
        });
    }
    
    // Refresh rates every 5 minutes
    setInterval(loadExchangeRates, 5 * 60 * 1000);
});

// Animate stats on scroll (keep existing functionality)
const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statNumbers = entry.target.querySelectorAll('.stat-number');
            statNumbers.forEach(stat => {
                const finalNumber = stat.textContent;
                const isPlus = finalNumber.includes('+');
                const number = parseInt(finalNumber.replace(/[^0-9]/g, ''));
                
                let current = 0;
                const increment = number / 50;
                const timer = setInterval(() => {
                    current += increment;
                    if (current >= number) {
                        stat.textContent = finalNumber;
                        clearInterval(timer);
                    } else {
                        stat.textContent = Math.floor(current) + (isPlus ? '+' : '');
                    }
                }, 30);
            });
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

const statsSection = document.querySelector('.stats');
if (statsSection) {
    observer.observe(statsSection);
}

