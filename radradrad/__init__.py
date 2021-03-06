import datetime
import json

import os
from collections import OrderedDict
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = '13e8ee0ac43c84afa0ec52751ab4ed47'
if os.path.isfile('config.json'):
    with open('config.json') as f:
        db_creds = json.load(f)
    db_url = 'mysql://{}:{}@{}/{}'.format(db_creds['username'],
                                          db_creds['password'],
                                          db_creds['host'],
                                          db_creds['db'])
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'db.sqlite'))
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config.from_object('config')

db = SQLAlchemy(app)
Bootstrap(app)
toolbar = DebugToolbarExtension(app)


def timestamp(date=None):
    """
    Return the current timestamp as an integer
    :return:
    """
    if date:
        return int(datetime.datetime.strptime(date, '%Y-%m-%d').timestamp())
    return int(datetime.datetime.utcnow().timestamp())


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
                   'location': 'sf'},
                  {'name': 'The Chapel Bar',
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
    created_at = db.Column(db.Integer, default=timestamp)
    date = db.Column(db.String(20))
    time = db.Column(db.String(80))
    url = db.Column(db.String(150))
    headliner = db.Column(db.String(180))
    supports = db.Column(db.Text)
    age = db.Column(db.String(80))
    cost = db.Column(db.String(80))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))

    db.UniqueConstraint(date, time, headliner)

    def __repr__(self):
        return '<Concert {} - {}>'.format(self.headliner, self.date)

    def concert_to_dict(concerts):
        """
        Takes input of list of Concert objects and returns dictionary of dates with concerts
        """
        concerts_by_date = {date: [] for date in set(concert.date for concert in concerts)}
        for concert in concerts:
            concerts_by_date[concert.date].append(concert)
        concerts_by_date = OrderedDict(sorted(concerts_by_date.items(), key=lambda t: t[0]))
        return concerts_by_date

    @staticmethod
    def date_range(date_start=None, date_end=None):
        """
        Returns next four weeks of concerts
        """
        # date_start = datetime.datetime.now(pytz.timezone('US/Pacific'))
        if date_start == None:
            date_start = datetime.datetime.utcnow()
        else:
            date_start = datetime.datetime.strptime(date_start, '%Y-%m-%d')
        if date_end == None:
            date_end = date_start + datetime.timedelta(weeks=4)
        else:
            date_end = datetime.datetime.strptime(date_end, '%Y-%m-%d')

        concerts = Concert.query.filter(Concert.date >= date_start.strftime('%Y-%m-%d'),
                                        Concert.date <= date_end.strftime('%Y-%m-%d'),
                                        Concert.url != None).order_by(Concert.date.asc())
        return concerts

    @staticmethod
    def added_today(return_dict=False):
        today = datetime.datetime.utcnow()
        tomorrow = today + datetime.timedelta(1)

        # today_timestamp = int(datetime.datetime(today.year, today.month, today.day).timestamp())
        today_timestamp = timestamp('{}-{}-{}'.format(today.year, today.month, today.day))
        tomorrow_timestamp = timestamp('{}-{}-{}'.format(tomorrow.year, tomorrow.month, tomorrow.day))
        concerts_added_today = Concert.query.filter(Concert.created_at >= today_timestamp,
                                                    Concert.created_at < tomorrow_timestamp)

        if return_dict:
            concerts = concerts_added_today.all()
            return Concert.concert_to_dict(concerts)

        return concerts_added_today

    @staticmethod
    def next_month_by_date():
        concerts = Concert.date_range().all()
        return Concert.concert_to_dict(concerts)

@app.template_filter('timestamp')
def timestamp_from_date(s):
    return timestamp(s)


@app.template_filter('display_date')
def display_date(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d').strftime('%A, %B %d, %Y')

@app.route('/')
def index():
    concerts = Concert.next_month_by_date()
    venues = Venue.query.order_by(Venue.name).all()
    added_today = Concert.added_today().count()
    return render_template('index.html', venues=venues, concerts=concerts, added_today=added_today)


@app.route('/venue/<int:venue_id>')
def venue(venue_id):
    venues = Venue.query.order_by(Venue.name).all()
    venue_concerts = Concert.query.filter(Concert.venue_id == venue_id).all()
    concerts = Concert.concert_to_dict(venue_concerts)
    added_today = Concert.added_today().count()
    return render_template('index.html', venues=venues, concerts=concerts, added_today=added_today)


@app.route('/new')
def new():
    venues = Venue.query.order_by(Venue.name).all()
    concerts_today = Concert.added_today(True)
    added_today = Concert.added_today().count()
    return render_template('index.html', venues=venues, concerts=concerts_today, added_today=added_today)
