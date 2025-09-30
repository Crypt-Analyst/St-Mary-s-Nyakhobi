# St. Mary's Nyakhobi Senior School Website - Setup Instructions
# MAROON & WHITE COLOR THEME APPLIED ✅

Write-Host "=== ST. MARY'S NYAKHOBI SENIOR SCHOOL WEBSITE SETUP ===" -ForegroundColor White -BackgroundColor DarkRed
Write-Host ""
Write-Host "Website colors updated to match school uniform:" -ForegroundColor DarkRed
Write-Host "  🔴 Maroon (trousers) - Primary navigation and headers" -ForegroundColor DarkRed
Write-Host "  ⚪ White (shirts) - Background and text areas" -ForegroundColor White
Write-Host ""

# Check if Python is installed
$pythonCheck = Get-Command python -ErrorAction SilentlyContinue
if ($pythonCheck) {
    Write-Host "✅ Python is installed" -ForegroundColor Green
    python --version
    
    Write-Host ""
    Write-Host "🔄 Setting up virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    
    Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
    
    Write-Host "🔄 Installing Django and dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    
    Write-Host "🔄 Setting up database..." -ForegroundColor Yellow
    python manage.py makemigrations
    python manage.py migrate
    
    Write-Host "🔄 Loading school data..." -ForegroundColor Yellow
    python manage.py loaddata sample_data.json
    
    Write-Host ""
    Write-Host "✅ Setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📝 NEXT STEPS:" -ForegroundColor Yellow
    Write-Host "1. Create admin account: python manage.py createsuperuser" -ForegroundColor Cyan
    Write-Host "2. Start website: python manage.py runserver" -ForegroundColor Cyan
    Write-Host "3. Visit: http://127.0.0.1:8000" -ForegroundColor Cyan
} else {
    Write-Host "❌ PYTHON NOT INSTALLED" -ForegroundColor Red -BackgroundColor Yellow
    Write-Host ""
    Write-Host "Please install Python first:" -ForegroundColor Red
    Write-Host "1. Visit: https://www.python.org/downloads/" -ForegroundColor Cyan
    Write-Host "2. Download Python 3.8 or newer" -ForegroundColor Cyan
    Write-Host "3. During installation, CHECK 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host "4. Restart your computer" -ForegroundColor Yellow
    Write-Host "5. Run this script again" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=== SCHOOL INFORMATION ALREADY CONFIGURED ===" -ForegroundColor White -BackgroundColor DarkRed
Write-Host "🏫 School: St. Mary's Nyakhobi Senior School" -ForegroundColor DarkRed
Write-Host "👨‍💼 Principal: Mr. Dan F. Olopi" -ForegroundColor DarkRed
Write-Host "📍 Location: Funyula, Busia County" -ForegroundColor DarkRed
Write-Host "📞 Phone: +254 722 231798 / +254 723 273109" -ForegroundColor DarkRed
Write-Host "✉️ Email: nyakhobisecondaryschool@gmail.com" -ForegroundColor DarkRed