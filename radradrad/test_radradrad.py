import datetime
import unittest

import os

from radradrad import app, db, Venue, Concert

basedir = os.path.abspath(os.path.dirname(__file__))

class ConcertTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()
        Venue.create_all()

        show_info = {"show_time": "9PM",
                     "show_url": "http://www.url.com",
                     "show_headliner": "Headliner {}",
                     "show_supports": None,
                     "show_age": "All Ages",
                     "show_cost": "Free"
                    }

        for days in range(35):
            date = (datetime.datetime.now()+datetime.timedelta(days))
            concert = Concert(date=date.strftime('%Y-%m-%d'),
                              created_at=int(datetime.datetime.now().timestamp()),
                              time=show_info['show_time'],
                              url=show_info['show_url'],
                              headliner=show_info['show_headliner'].format(days),
                              supports=show_info['show_supports'],
                              age=show_info['show_age'],
                              cost=show_info['show_cost'],
                              venue_id=1)
            db.session.add(concert)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.unlink(os.path.join(basedir, 'test.db'))

    def min_date(self, query):
        """
        Returns min/first/start date of Concert query
        """
        return min(query.all(), key=lambda x: x.date)

    def max_date(self, query):
        """
        Returns max/last/end date of Concert query
        """
        return max(query.all(), key=lambda x: x.date)

    def test_date_range_without_args_returns_29(self):
        rv = Concert.date_range()
        assert rv.count() == 29

    def test_date_range_without_args_returns_correct_start_date(self):
        rv = Concert.date_range()
        start_date = self.min_date(rv).date
        expected = datetime.datetime.now().strftime('%Y-%m-%d')
        assert start_date == expected

    def test_date_range_without_args_returns_correct_end_date(self):
        rv = Concert.date_range()
        end_date = self.max_date(rv).date
        expected = (datetime.datetime.now() + datetime.timedelta(28)).strftime('%Y-%m-%d')
        assert end_date == expected

    def test_date_range_returns_count_with_args(self):
        start_date = "2016-09-13"
        end_date = "2016-09-23"
        rv = Concert.date_range(start_date, end_date)
        assert rv.count() == 11

    def test_date_range_returns_start_date_with_args(self):
        start_date = "2016-09-13"
        end_date = "2016-09-23"
        rv = Concert.date_range(start_date, end_date)
        assert self.min_date(rv).date == start_date

    def test_date_range_returns_end_date_with_args(self):
        start_date = "2016-09-13"
        end_date = "2016-09-23"
        rv = Concert.date_range(start_date, end_date)
        assert self.max_date(rv).date == end_date