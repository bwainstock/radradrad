from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
