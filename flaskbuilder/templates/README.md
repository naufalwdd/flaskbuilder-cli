# FIRST MIGRATION

$env:FLASK_APP = "main.py"  # PowerShell
set FLASK_APP=main # CMD

set FLASK_APP=main.py
flask db init
flask db migrate -m "Add user table"
flask db upgrade