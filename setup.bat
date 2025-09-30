@echo off
echo ===================================================================
echo   ST. MARY'S NYAKHOBI SENIOR SCHOOL WEBSITE
echo   MAROON ^& WHITE THEME APPLIED (School Uniform Colors)
echo ===================================================================
echo.

echo Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python first:
    echo 1. Go to: https://www.python.org/downloads/
    echo 2. Download Python 3.8 or newer
    echo 3. During installation, CHECK "Add Python to PATH"
    echo 4. Restart your computer
    echo 5. Run this script again
    echo.
    pause
    exit /b 1
)

echo [SUCCESS] Python is installed!
python --version

echo.
echo Setting up virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing Django and dependencies...
pip install -r requirements.txt

echo.
echo Setting up database...
python manage.py makemigrations
python manage.py migrate

echo.
echo Loading school data...
python manage.py loaddata sample_data.json

echo.
echo ===================================================================
echo   SETUP COMPLETE!
echo ===================================================================
echo.
echo NEXT STEPS:
echo 1. Create admin account: python manage.py createsuperuser
echo 2. Start website: python manage.py runserver
echo 3. Visit: http://127.0.0.1:8000
echo.
echo SCHOOL INFORMATION CONFIGURED:
echo - School: St. Mary's Nyakhobi Senior School
echo - Principal: Mr. Dan F. Olopi
echo - Location: Funyula, Busia County
echo - Colors: Maroon ^& White (uniform colors)
echo.
pause