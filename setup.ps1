# St. Mary's School Website Setup Script

# Step 1: Install Python (if not already installed)
# Download and install Python 3.8+ from https://www.python.org/downloads/
# Make sure to check "Add Python to PATH" during installation

# Step 2: Create and activate virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Green
python -m venv venv
venv\Scripts\Activate.ps1

# Step 3: Install required packages
Write-Host "Installing required packages..." -ForegroundColor Green
pip install -r requirements.txt

# Step 4: Run database migrations
Write-Host "Running database migrations..." -ForegroundColor Green
python manage.py makemigrations
python manage.py migrate

# Step 5: Create superuser (admin account)
Write-Host "Creating superuser account..." -ForegroundColor Green
Write-Host "Please enter your admin credentials:" -ForegroundColor Yellow
python manage.py createsuperuser

# Step 6: Collect static files
Write-Host "Collecting static files..." -ForegroundColor Green
python manage.py collectstatic --noinput

# Step 7: Load sample data (optional)
Write-Host "Loading sample data..." -ForegroundColor Green
python manage.py loaddata sample_data.json

# Step 8: Start development server
Write-Host "Starting development server..." -ForegroundColor Green
Write-Host "Access your website at: http://127.0.0.1:8000/" -ForegroundColor Cyan
Write-Host "Access admin panel at: http://127.0.0.1:8000/admin/" -ForegroundColor Cyan
python manage.py runserver