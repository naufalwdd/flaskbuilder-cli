# FIRST MIGRATION

set FLASK_APP=main.py
flask db init
flask db migrate -m "Add user table"
flask db upgrade