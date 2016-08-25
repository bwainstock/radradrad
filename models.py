from calendar import Calendar
import datetime
import itertools
import os
import pytz

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'db.sqlite'))
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app, session_options={"autoflush": False})
db = SQLAlchemy(app)


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    location = db.Column(db.String(80))
    concerts = db.relationship('Concert', backref='venue', lazy='dynamic')

#    def __init__(self, name, location):
#        self.name = name
#        self.location = location

    def __repr__(self):
        return '<Venue {} - {}>'.format(self.name, self.location)


class Concert(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    time = db.Column(db.String(80))
    url = db.Column(db.String(150))
    headliner = db.Column(db.String(80))
    supports = db.Column(db.Text)
    age = db.Column(db.String(80))
    cost = db.Column(db.String(80))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))

    db.UniqueConstraint(date, time, headliner)
#    def __init__(self, date, time, url, headliner, supports, age, cost, venue_id):
#        self.date = date
#        self.time = time
#        self.url = url
#        self.headliner = headliner
#        self.supports = supports
#        self.age = age
#        self.cost = cost
#        self.location = location

    def __repr__(self):
        return '<Concert {} - {}>'.format(self.headliner, self.date)

    @staticmethod
    def next_month():
        date_start = datetime.datetime.now(pytz.timezone('US/Pacific'))
        date_end = date_start + datetime.timedelta(weeks=4)
        concerts = Concert.query.filter(Concert.date >= date_start,
                                        Concert.date <= date_end).all()
        return concerts
