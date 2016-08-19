import unittest

import scrapers

class TheChapelTestCase(unittest.TestCase):

    def test_the_chapel_get(self):
        try:
            chapel_shows = scrapers.chapel()
        except:
            self.fail("Could not fetch Chapel shows")
