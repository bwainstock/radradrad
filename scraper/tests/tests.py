import unittest
import datetime
import os
from bs4 import BeautifulSoup
import scraper


basedir = os.path.abspath(os.path.dirname(__file__))

class TheChapelTestCase(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(basedir, 'chapel_test_show.html'), 'r') as f:
            self.show = BeautifulSoup(f.read(), 'html.parser')

#    def test_the_chapel_get(self):
#        try:
#            scrapers.chapel()
#        except:
#            self.fail("Could not fetch Chapel shows")

    def test_parse_chapel(self):
        show_date = datetime.datetime(2016, 8, 25, 0, 0)
        parsed_show = scraper.parse_chapel(show_date, self.show)
        expected_output = {'show_age': 'All Ages',
                           'show_cost': None,
                           'show_date': datetime.datetime(2016, 8, 25, 0, 0),
                           'show_headliner': 'Diane Coffee',
                           'show_location': 'The Chapel',
                           'show_supports': ['Waterstrider', 'Doncat'],
                           'show_time': '8:30 pm',
                           'show_url':
                           'http://www.thechapelsf.com/event/1182569-diane-coffee-san-francisco/'}
        self.assertEqual(parsed_show, expected_output)


class BottomOfTheHillTestCase(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(basedir, 'both_test_show.html'), 'r') as f:
            self.show = BeautifulSoup(f.read(), 'html.parser')

    def test_parse_both(self):
        parsed_show = scraper.parse_both(self.show)
        expected_output = {'show_age': 'ALL AGES',
                           'show_cost': '$15 in advance / $17 at the door',
                           'show_date': datetime.datetime(2016, 8, 24, 0, 0),
                           'show_headliner': 'Turnover',
                           'show_location': 'Bottom of the Hill',
                           'show_supports': ['Angel Dust', 'Triathalon'],
                           'show_time': '8:00PM doors -- music at 9:00PM ',
                           'show_url':
                           'http://www.bottomofthehill.com/20160824.html'}
        self.assertEqual(parsed_show, expected_output)
