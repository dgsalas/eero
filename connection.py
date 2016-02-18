__author__ = 'dgsalas'
""" """

from config import Config
from sqlalchemy import create_engine
from flask import Flask
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import MetaData


ENGINES = {}

def get_engine(conn_str):
    """
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

metadata = MetaData()

base.metadata.create_all(engine)

# create our little application :)
app = Flask(__name__)
app.debug = settings.debug
app.config.from_object(__name__)

@app.route('/')
@app.route('/<url>/')
def process_view(url=None):
    """  """
    from model import Pages
    if url is None:
        text = 'processing home'
        url = '/'
    else:
        text = "Processing view {}".format(url)
        url = '/' + url + '/'

    print url
    page = session.query(Pages).filter(Pages.url == url).first()

    if page is None:
        text = '404'

    return text

if __name__ == '__main__':
    from model import setup_database, Pages, Sections, PagesSections, ImageTypes, Clients, Users, Projects, \
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
