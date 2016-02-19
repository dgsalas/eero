# -*- coding: utf-8 -*-
""" Connection to the database 0"""

__author__ = 'dgsalas'

from config import Config
from sqlalchemy import create_engine
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy


ENGINES = {}


def get_engine(conn_str):
    """
    :param conn_str = Connexion string
    """
    global ENGINES
    e = ENGINES.get(conn_str)
    if e is None:
        e = create_engine(conn_str, pool_size=50)
        ENGINES[conn_str] = e

    return e

f = file('settings.cfg')
settings = Config(f)
engine = get_engine(settings.conn_str)
Session = sessionmaker(bind=engine)
session = Session()
base = declarative_base()

base.metadata.create_all(engine)

app = Flask(__name__)
app.debug = settings.debug
app.config.from_object(__name__)

db = SQLAlchemy(app)

@app.route('/')
@app.route('/<url>/')
def process_view(url=None):
    """
    :param url: URL Received in the call

    """
    from model import Pages
    if url is None:
        text = 'processing home <br>'
        url = '/'
    else:
        text = "Processing view {}<br>".format(url)
        url = '/' + url + '/'

    print url
    page = session.query(Pages).filter(Pages.url == url).first()

    for section in page.sections:
        print section.name
        text += '<br>'+section.name

    if page is None:
        text = '404'

    return text

if __name__ == '__main__':
    from model import setup_database, Pages, Sections, ImageTypes, Clients, Users, Projects, \
        Rooms, Hours, Images
    admin = Admin(app, name='eero', template_mode='bootstrap3')

    admin.add_view(ModelView(Pages, session))
    admin.add_view(ModelView(Sections, session))
    admin.add_view(ModelView(Clients, session))
    admin.add_view(ModelView(Users, session))
    admin.add_view(ModelView(Projects, session))
    admin.add_view(ModelView(Rooms, session))
    admin.add_view(ModelView(Hours, session))
    admin.add_view(ModelView(Images, session))
    admin.add_view(ModelView(ImageTypes, session))

    setup_database()

    app.run()
