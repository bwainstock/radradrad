'''Collection of functions to scrape various concert calendars'''

from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup


def _get_soup(url):
    '''
    Return soup of calendar
    '''
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    return soup


def chapel():
    '''
    Scrapes calendar information from The Chapel SF website.
    '''
    chapel_shows = []
    base_url = 'http://www.thechapelsf.com'
    calendar_url = ''.join([base_url, '/calendar/'])

    soup = _get_soup(calendar_url)

    show_calendar = soup.findAll(class_='vevent')
    for day in show_calendar:
        show_date = day.find('span', class_='value-title').get('title')
        show_date = re.search(r"([0-9-])+", show_date).group()
        show_date = datetime.strptime(show_date, '%Y-%m-%d')

        shows = day.findAll('div', class_='one-event')
        for show in shows:
            show_url = show.find(class_='url')
            if show_url:
                show_headliner = show_url.text
            show_url = ''.join([base_url, show_url.get('href')])
            show_supports = show.findAll(class_='supports')
            if show_supports:
                show_supports = [supports.text for supports in show_supports]
            show_time = show.find(class_='start-time')
            if show_time:
                show_time = show_time.text
            show_location = show.find(class_='venue')
            if show_location:
                show_location = show_location.text
            show_age_restrictions = show.find(class_='age-restriction')
            if show_age_restrictions:
                show_age_restrictions = show_age_restrictions.text
            show_free = show.find(class_='free')
            if show_free:
                show_free = True

            show_info = {
                'show_date': show_date,
                'show_time': show_time,
                'show_url': show_url,
                'show_headliner': show_headliner,
                'show_supports': show_supports,
                'show_location': show_location,
                'show_age_restrictions': show_age_restrictions,
                'show_free': show_free
                }
            chapel_shows.append(show_info)

    return chapel_shows


def both():
    '''
    Scrapes calendar information from Bottom of the Hill website.
    '''

    both_shows = []
    base_url = 'http://www.bottomofthehill.com'
    calendar_url = ''.join([base_url, '/calendar.html'])

    soup = _get_soup(calendar_url)

    show_calendar = soup.find('table', id='listings')
    for show in show_calendar:
        if show.find(class_='date'):
            show = show.find(style=re.compile(r'vertical-align: top'))

            show_url = show.find('a').get('href')
            bands = show.findAll(class_='band')
            show_headliner = bands[0].text
            show_supports = [band.text for band in bands[1:]]

            show_date = [date.text for date in show.findAll(class_='date')]
            show_date = datetime.strptime(show_date, '%A %B %d %Y')

            show_info = {
                'show_date': show_date,
                # 'show_time': show_time,
                'show_url': show_url,
                'show_headliner': show_headliner,
                'show_supports': show_supports,
                # 'show_location': show_location,
                # 'show_age_restrictions': show_age_restrictions,
                # 'show_free': show_free
                }
            both_shows.append(show_info)

    return both_shows
