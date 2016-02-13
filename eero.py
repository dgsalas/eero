# all the imports
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing
from model import Pages

# configuration
DATABASE = '/home/desarrollo/eero/eero.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_envvar('EERO_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['EERO'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('eero.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == '__main__':
    app.run()