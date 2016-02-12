__author__ = 'dgsalas'

from flask import Flask
from flask_sqlalchemy import SQL_Alchemy, create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sysdba:master@localhost:5432/eero'
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
        return '<Page {}, Sectiom {}, Order {}>'.format(self.page.name, self.section.name, self.order)


class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80), unique=True)
    address = db.Column(db.Text)
    city = db.Column(db.String(80))
    zipcode = db.Column(db.String(10))
    email = db.Column(db.String(40))

    def __init__(self, name, address, city, zipcode, email):
        self.name = name
        self.address = address
        self.city = city
        self.zipcode = zipcode
        self.email = email

    def __repr__(self):
        user = db.session.query(self.user).one
        return '<Client {} User {}>'.format(self.name, user.name)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    login = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(128))

    client_id = db.Column(db.Integer, db.ForeignKey('Clients.id'))
    client = db.relationship('Clients', backref=db.backref('client'), lazy='dynamic')

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
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(40), unique=True)

    client_id = db.Column(db.Integer, db.ForeignKey('Clients.id'))
    client = db.relationship('Clients', backref=db.backref('client'), lazy='dynamic')

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
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = db.relationship('Users', backref=db.backref('user'), lazy='dynamic')

    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    finish_time = db.Column(db.Time)
    time = db.Column(db.Integer)

    create_invoice = db.Column(db.Boolean)

    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.id'))
    room = db.relationship('Rooms', backref=db.backref('hours'), lazy='dynamic')

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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<ImageType {}>'.format(self.name)


class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    extension = db.Column(db.String(5))

    room_id = db.Column(db.Integer, db.ForeignKey('Rooms.id'))
    room = db.relationship('Rooms', backref=db.backref('hours'), lazy='dynamic')

    image_type = db.Column(db.Integer, db.ForeignKey('ImageTypes.id'))
    type = db.relationship('ImageTypes', backref=db.backref('images'), lazy='dynamic')

    def __init__(self, name, extension, room_id, type_id):
        self.name = name
        self.extension = extension
        self.room_id = room_id
        self.type_id = type_id

    def __repr__(self):
        return 'Image {}, Room {}, Project {}, Client {}'.format(self.name, self.room.name,
                                                                 self.room.project.name, self.client.name)
