from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup


def chapel():
    '''
    Scrapes calendar information from The Chapel SF website.
    '''
    chapel_shows = []
    base_url = 'http://www.thechapelsf.com'
    calendar_url = ''.join([base_url, '/calendar/'])

    resp = requests.get(calendar_url)
    soup = BeautifulSoup(resp.content, 'html.parser')

    show_calendar = soup.findAll(class_='vevent')
    for day in show_calendar:
        date = day.find('span', class_='value-title').get('title')
        date = re.search(r"([0-9-])+", date).group()
        date = datetime.strptime(date, '%Y-%m-%d')

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

            show_info = {'show_date': date,
                         'show_time': show_time,
                         'show_url': show_url,
                         'show_headliner': show_headliner,
                         'show_supports': show_supports,
                         'show_location': show_location,
                         'show_age_restrictions': show_age_restrictions,
                         'show_free': show_free}
            chapel_shows.append(show_info)

    return chapel_shows
