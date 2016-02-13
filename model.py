# -*- coding: utf-8 -*-
__author__ = 'dgsalas'

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, relation
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Date, Text, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from eero import app

ENGINES = {}
def get_engine(conn_str):
    """
    Singleton que devuelve un engine a partir de una cadena de conexión (conn_str).
    Si conn_str ya ha sido usado se devuelve el existente de tal forma que globalmente
    existe un único engine por cada cadena de conexión (o por cada database que es lo mismo)
    """
    global ENGINES
    e = ENGINES.get(conn_str)
    if e is None:
        e = create_engine(conn_str, pool_size=50) #, poolclass=SingletonThreadPool, pool_size=50, pool_recycle=30)
        ENGINES[conn_str] = e

    return e

engine = get_engine('postgresql://postgres@localhost:5432/eero')
Session = sessionmaker(bind=engine)
session = Session()
base = declarative_base()

db = SQLAlchemy(app)


class Pages(base):
    """ Pages of the site (would it be better to use a CMS?)  """
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    home = Column(Boolean, unique=True)

    def __init__(self, name, home):
        self.name = name
        self.home = home

    def __repr__(self):
        return '<Page {}>'.format(self.name)


class Sections(base):
    """ Section of the site. As you can see, it's a M to N relationship  """
    __tablename__ = 'sections'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Section {}>'.format(self.name)


class PagesSections(base):
    """ Table bewteen Pages and Sections  """
    __tablename__ = 'pagessections'
    id = Column(Integer, primary_key=True)

    page_id = Column(Integer, ForeignKey(Pages.id))
    page = relation(Pages, backref='pages')

    section_id = Column(Integer, ForeignKey(Sections.id))
    section = relation('Sections', backref='sections')

    def __init__(self, page_id, section_id, order):
        self.page_id = page_id
        self.section_id = section_id
        self.order = order

    def __repr__(self):
        return '<Page {}, Section {}, Order {}>'.format(self.page.name, self.section.name, self.order)


class Clients(base):
    """ Clients of the company  """
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)

    name = Column(String(80), unique=True)
    address = Column(Text)
    city = Column(String(80))
    zipcode = Column(String(10))
    email = Column(String(40))

    # user_id = Column(Integer, ForeignKey(Users.id))
    # user = relation('Users', backref='user')

    def __init__(self, name, address, city, zipcode, email):
        self.name = name
        self.address = address
        self.city = city
        self.zipcode = zipcode
        self.email = email

    def __repr__(self):
        return '<Client {} User {}>'.format(self.name, self.user.name)


class Users(base):
    """ Users of the system  """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    login = Column(String(20), unique=True)
    password = Column(String(128))

    client_id = Column(Integer, ForeignKey(Clients.id))
    client = relation('Clients', backref='user')

    def __init__(self, login, password, client_id=None):
        self.login = login
        self.password = password
        self.client_id = client_id

    def __repr__(self):
        if self.client_id is None:
            return 'User {}'.format(self.login)
        else:
            return 'User {}, Client {}'.format(self.login, self.client.name)


class Projects(base):
    """ Projects of the company  """
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)

    name = Column(String(40), unique=True)

    client_id = Column(Integer, ForeignKey(Clients.id))
    client = relation('Clients', backref='client')

    def __init__(self, name, client_id):
        self.name = name
        self.client_id = client_id

    def __repr__(self):
        return 'Project {}, Client {}'.format(self.name, self.client.name)


class Rooms(base):
    """ Rooms of the project  """
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)

    name = Column(String(40))

    project_id = Column(Integer, ForeignKey(Projects.id))
    project = relation('Projects')

    def __init__(self, name, project_id):
        self.name = name
        self.project_id = project_id

    def __repr__(self):
        return 'Room {} Project {}, Client {}'.format(self.name, self.project.name, self.client.name)


class Hours(base):
    """ Hours worked  """
    __tablename__ = 'hours'
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey(Users.id))
    user = relation('Users', backref='user')

    date = Column(Date)
    start_time = Column(Time)
    finish_time = Column(Time)
    time = Column(Integer)

    create_invoice = Column(Boolean)

    room_id = Column(Integer, ForeignKey(Rooms.id))
    room = relation('Rooms', backref='hours')

    def __init__(self, user_id, date, start_time, finish_time, time, create_invoice=None, room_id=None):
        self.user_id = user_id
        self.date = date
        self.start_time = start_time
        self.finish_time = finish_time
        self.time = time
        self.create_invoice = create_invoice
        self.room_id = room_id

    def __repr__(self):
        if self.room_id is None:
            return '{} Hours, {} User'.format(self.time, self.user.login)
        else:
            return '{} Hours, {} User, {} Room, {} Project {}'.format(self.time, self.user.name,
                                                                      self.room.name, self.room.project.name)


class ImageTypes(base):
    """ Types of images """
    __tablename__= 'imagetypes'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<ImageType {}>'.format(self.name)


class Images(base):
    """ Images of the room  """
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)

    name = Column(String(100))
    extension = Column(String(5))

    room_id = Column(Integer, ForeignKey(Rooms.id))
    room = relation('Rooms')

    type_id = Column(Integer, ForeignKey(ImageTypes.id))
    type = relation('ImageTypes')

    private = Column(Boolean)

    def __init__(self, name, extension, private, room_id, type_id):
        self.name = name
        self.extension = extension
        self.private = private
        self.room_id = room_id
        self.type_id = type_id

    def __repr__(self):
        return 'Image {}, Room {}, Project {}, Client {}'.format(self.name, self.room.name,
                                                                 self.room.project.name, self.client.name)

if __name__ == "__main__":

    # Si no hay tipos de imágenes, inicializamos la base de datos
    base.metadata.create_all(engine)
    print(session.query(ImageTypes).count())
    if session.query(ImageTypes).count() == 0:
        tipo = ImageTypes('Idea')
        session.add(tipo)
        tipo = ImageTypes('Render')
        session.add(tipo)
        print('OK!')
        session.commit()

