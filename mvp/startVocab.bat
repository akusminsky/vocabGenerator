@echo off
cd C:\Users\andre\OneDrive\Escritorio\Code\misApps\vocabGenerator\mvp
set FLASK_APP=back1_1.py

REM Start Flask server in the background
start /b C:\Users\andre\AppData\Local\Programs\Python\Python311\python.exe -m flask run

REM Open HTML file in default browser
start "" "C:\Users\andre\OneDrive\Escritorio\Code\misApps\vocabGenerator\mvp\front1.1.html"

pause
