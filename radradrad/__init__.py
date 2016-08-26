import datetime

import os
import pytz
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '13e8ee0ac43c84afa0ec52751ab4ed47'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'db.sqlite'))
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config.from_object('config')

db = SQLAlchemy(app)
Bootstrap(app)
toolbar = DebugToolbarExtension(app)


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

    @staticmethod
    def create_all():
        changed = False
        venues = [{'name': 'The Chapel',
                   'location': 'sf'},
                  {'name': 'The Vestry',
                   'location': 'sf'},
                  {'name': 'Bottom of the Hill',
                   'location': 'sf'}]
        for venue in venues:
            venue_entry = Venue.query.filter_by(name=venue['name'],
                                                location=venue['location']).first()
            if venue_entry is None:
                db.session.add(Venue(name=venue['name'],
                                     location=venue['location']))
                changed = True
        if changed:
            db.session.commit()


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

    def __repr__(self):
        return '<Concert {} - {}>'.format(self.headliner, self.date)

    @staticmethod
    def next_month():
        """
        Returns next four weeks of concerts
        """
        date_start = datetime.datetime.now(pytz.timezone('US/Pacific'))
        date_end = date_start + datetime.timedelta(weeks=4)
        concerts = Concert.query.filter(Concert.date >= date_start,
                                        Concert.date <= date_end).order_by(Concert.date.asc())
        return concerts

    @staticmethod
    def next_month_by_date():
        concerts = Concert.next_month().all()
        concerts_by_date = {date: [] for date in set(concert.date for concert in concerts)}
        for concert in concerts:
            concerts_by_date[concert.date].append(concert)

        return concerts_by_date


@app.route('/')
def index():
    concerts = Concert.next_month_by_date()
    return render_template('index.html', concerts=concerts)
