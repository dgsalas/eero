# -*- coding: utf-8 -*-
""" """
__author__ = 'dgsalas'

from sqlalchemy.orm import relation
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Date, Text, Boolean, Time
from connection import base, session, db


# This is a third association/helper table
# posttags = db.Table('posttags',
#                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
#                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
#                     )
#
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.Text)
#     phone_number = db.Column(db.String(50))
#
#     tags= db.relationship('Tag', backref='posts', lazy='dynamic')
#
# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))

pagessections = db.Table('pagessections',
                         db.Column('page_id', db.Integer, db.ForeignKey('pages.id')),
                         db.Column('section_id', db.Integer, db.ForeignKey('sections.id'))
                         )

class Pages(db.Model):
    """ Pages of the site (would it be better to use a CMS?)  """
    __tablename__ = 'pages'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    home = db.Column(db.Boolean)
    url = db.Column(db.String(50), unique=True)

    # sections = relationship('Sections', backref='sections', lazy='dynamic')
    # sections = relationship('Sections', secondary=PagesSections, backref=backref('sections', lazy='dynamic'))
    # sections = relationship("Sections", secondary=PagesSections)

    sections = db.relationship('Sections', secondary=pagessections)

    def __init__(self, name, home, url):
        self.name = name
        self.home = home
        self.url = url

    def __repr__(self):
        return '<Page {}>'.format(self.name)


class Sections(db.Model):
    """ Section of the site. As you can see, it's a M to N relationship  """
    __tablename__ = 'sections'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(80), unique=True)

    # pages = relationship(
    #     "Pages",
    #     secondary=PagesSections,
    #     back_populates="sections")

    pages = db.relationship('Pages', secondary=pagessections)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Section {}>'.format(self.name)


class Clients(base):
    """ Clients of the company  """
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)

    name = Column(String(80), unique=True)
    address = Column(Text)
    city = Column(String(80))
    zipcode = Column(String(10))
    email = Column(String(40))

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
    __tablename__ = 'imagetypes'
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

def setup_database():
    """
    If there's no image types, let's setup the database with initial objects
    """
    if session.query(ImageTypes).count() == 0:
        image_type = ImageTypes('Idea')
        session.add(image_type)
        image_type = ImageTypes('Render')
        session.add(image_type)

        page = Pages('Home', True, '/')
        session.add(page)

        page = Pages('Products', False, '/products/')
        session.add(page)

        page = Pages('Services', False, '/services/')
        session.add(page)

        print('OK!')
        session.commit()


