'''Collection of functions to scrape various concert calendars'''

from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup

from models import db, Venue, Concert


def _get_soup(url):
    '''
    Return soup of calendar
    '''
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    return soup


def insert_concert(show_info):
    '''
    Insert concert information into DB
    '''

    venue = Venue.query.get(1)
    concert = Concert(date=show_info['show_date'],
                      time=show_info['show_time'],
                      url=show_info['show_url'],
                      headliner=show_info['show_headliner'],
                      supports=','.join(show_info['show_supports']),
                      age=show_info['show_age'],
                      cost=show_info['show_cost'],
                      venue=venue)
    db.session.add(concert)


def parse_chapel(show_date, raw_show):
    '''
    Parses shows for The Chapel SF
    '''
    show = raw_show
    base_url = 'http://www.thechapelsf.com'
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
    show_age = show.find(class_='age-restriction')
    if show_age:
        show_age = show_age.text
    show_cost = show.find(class_='free')
    if show_cost:
        show_cost = 'Free'

    show_info = {
        'show_date': show_date,
        'show_time': show_time,
        'show_url': show_url,
        'show_headliner': show_headliner,
        'show_supports': show_supports,
        'show_location': show_location,
        'show_age': show_age,
        'show_cost': show_cost
        }

    return show_info


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
            show_info = parse_chapel(show_date, show)
            chapel_shows.append(show_info)
            insert_concert(show_info)

    db.session.commit()

    return chapel_shows


def parse_both(raw_show):
    '''
    Parse show information for Bottom of the Hill
    '''

    regex = r'vertical-align: top; background-color'
    show = raw_show.find(style=re.compile(regex))

    bands = show.findAll(class_='band')
    if bands:
        show_headliner = bands[0].text
        print(show_headliner)
        if len(bands) > 1:
            show_supports = [band.text for band in bands[1:]]
    show_url = show.find('a')
    if show_url:
        show_url = show_url.get('href')

    show_date = [date.text for date in show.findAll(class_='date')]
    if show_date:
        show_date = ''.join(show_date).strip('\n')
        show_date = datetime.strptime(show_date, '%A %B %d %Y')

    show_time = ''.join([x.text for x in show.findAll(class_='time')])
    if show_time:
        show_time = show_time.replace('\n', ' ')

    show_location = 'Bottom of the Hill'

    show_age = show.findAll(class_='age')
    if show_age:
        show_age = [x.text for x in show_age if '\n' not in x.text]
        show_age = ''.join(show_age)

    show_cost = show.findAll(class_='cover')
    if show_cost:
        show_cost = ''.join([x.text for x in show_cost])
        show_cost = show_cost.replace('\n', ' ')

    show_info = {
        'show_date': show_date,
        'show_time': show_time,
        'show_url': show_url,
        'show_headliner': show_headliner,
        'show_supports': show_supports,
        'show_location': show_location,
        'show_age': show_age,
        'show_cost': show_cost
        }

    return show_info


def both():
    '''
    Scrapes calendar information from Bottom of the Hill website.
    '''

    both_shows = []
    base_url = 'http://www.bottomofthehill.com'
    calendar_url = ''.join([base_url, '/calendar.html'])

    soup = _get_soup(calendar_url)

    show_calendar = soup.find('table', id='listings').findAll('tr')
    for show in show_calendar:
        if show.find(class_='date'):
            show_info = parse_both(show)
            both_shows.append(show_info)
            insert_concert(show_info)

    db.session.commit()
    return both_shows


def main():
    db.create_all()
    chapel()
    both()


if __name__ == '__main__':
    main()
