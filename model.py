# -*- coding: utf-8 -*-
__author__ = 'dgsalas'

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from eero import app

engine = create_engine('postgresql://postgres@localhost:5432/eero', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

db = SQLAlchemy(app)

class Pages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    home = db.Column(db.Boolean, unique=True)

    def __init__(self, name, home):
        self.name = name
        self.home = home

    def __repr__(self):
        return '<Page {}>'.format(self.name)


class Sections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Section {}>'.format(self.name)


class PagesSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_id = db.Column(db.Integer, db.ForeignKey('pages.id'))
    page = db.relationship('Pages', backref=db.backref('pages', lazy='dynamic'))
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
    section = db.relationship('Sections', backref=db.backref('sections', lazy='dynamic'))

    def __init__(self, page_id, section_id, order):
        self.page_id = page_id
        self.section_id = section_id
        self.order = order

    def __repr__(self):
        return '<Page {}, Section {}, Order {}>'.format(self.page.name, self.section.name, self.order)


class Clients(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), unique=True)
    address = db.Column(db.Text)
    city = db.Column(db.String(80))
    zipcode = db.Column(db.String(10))
    email = db.Column(db.String(40))

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship('Users', backref='user')

    def __init__(self, name, address, city, zipcode, email):
        self.name = name
        self.address = address
        self.city = city
        self.zipcode = zipcode
        self.email = email

    def __repr__(self):
        return '<Client {} User {}>'.format(self.name, self.user.name)


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    login = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(128))

    client_id = db.Column(db.Integer, db.ForeignKey('Clients.id'))
    client = db.relationship('Clients', backref='user')

    def __init__(self, login, password, client_id=None):
        self.login = login
        self.password = password
        self.client_id = client_id

    def __repr__(self):
        if self.client_id is None:
            return 'User {}'.format(self.login)
        else:
            return 'User {}, Client {}'.format(self.login, self.client.name)


class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(40), unique=True)

    client_id = db.Column(db.Integer, db.ForeignKey('Clients.id'))
    client = db.relationship('Clients', backref='client')

    def __init__(self, name, client_id):
        self.name = name
        self.client_id = client_id

    def __repr__(self):
        return 'Project {}, Client {}'.format(self.name, self.client.name)


class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(40))

    project_id = db.Column(db.Integer, db.ForeignKey('Projects.id'))
    project = db.relationship('Project', backref=db.backref('project'), lazy='dynamic')

    def __init__(self, name, project_id):
        self.name = name
        self.project_id = project_id

    def __repr__(self):
        return 'Project {}, Client {}'.format(self.name, self.client.name)


class Hours(db.Model):
    __tablename__ = 'hours'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship('Users', backref='user')

    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    finish_time = db.Column(db.Time)
    time = db.Column(db.Integer)

    create_invoice = db.Column(db.Boolean)

    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.id'))
    room = db.relationship('Rooms', backref='hours')

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
                                                                      self.room.name, self.room.projedct.mname)


class ImageTypes(db.Model):
    __tablename__= 'imagetypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<ImageType {}>'.format(self.name)


class Images(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    extension = db.Column(db.String(5))

    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.id'))
    room = db.relationship('Rooms', backref='hours')

    type_id = db.Column(db.Integer, db.ForeignKey('ImageTypes.id'))
    type = db.relationship('ImageTypes', backref='images')

    private = db.Column(db.Boolean)

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
    if db.session.query(ImageTypes).count == 0:
        tipo = ImageTypes('Idea')
        db.session.add(tipo)
        tipo = ImageTypes('Render')
        db.session.add(tipo)