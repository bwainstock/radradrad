import unittest
import datetime
from bs4 import BeautifulSoup
import scrapers


class TheChapelTestCase(unittest.TestCase):

    def test_the_chapel_get(self):
        try:
            scrapers.chapel()
        except:
            self.fail("Could not fetch Chapel shows")


class BottomOfTheHillTestCase(unittest.TestCase):

    def setUp(self):
        with open('./tests/both_test_show.html', 'r') as f:
            self.show = BeautifulSoup(f.read(), 'html.parser')

    def test_parse_both(self):
        parsed_show = scrapers.parse_both(self.show)
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
