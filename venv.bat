SET CWD=%~DP0
SET ENV=.venv

rmdir /S /Q "%CWD%%ENV%"
"C:/Python311/python.exe" -m venv "%CWD%%ENV%"

"%CWD%%ENV%/Scripts/pip" install --upgrade psycopg2-binary python-dotenv python-crontab

pause