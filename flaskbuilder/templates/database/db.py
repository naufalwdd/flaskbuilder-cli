from flask import g
import sqlite3
from config import Config

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(Config.DATABASE_PATH)
        g.db.row_factory = sqlite3.Row  # To access columns by name
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
        
def map_data(datas):
    data = []
    
    for user in datas:
        body = {key: user[key] for key in user.keys()}
        data.append(body)
        
    return data