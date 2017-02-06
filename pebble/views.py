import locale
from datetime import date, datetime
from math import ceil, floor
from subprocess import check_output

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse

import requests
from pytz import timezone, utc

TZ = timezone(settings.TIME_ZONE)
TOULOUSE = (43.604482, 1.443962)


def get_weather(lat, lon):
    wf = cache.get('pebble_wf')
    if wf is None:
        forecast = requests.get('http://api.openweathermap.org/data/2.5/forecast',
                                {'units': 'metric', 'lang': 'fr', 'lat': lat, 'lon': lon, 'appid': settings.OWM_KEY,
                                 'cnt': round((24 - datetime.now().hour) / 3)})
        weather = requests.get('http://api.openweathermap.org/data/2.5/weather',
                               {'units': 'metric', 'lang': 'fr', 'lat': lat, 'lon': lon, 'appid': settings.OWM_KEY})
        if weather.status_code != 200 or forecast.status_code != 200:
            return {}
        forecast = forecast.json()['list']
        weather = weather.json()
        cache.set('pebble_wf', (weather, forecast), 900)
    else:
        weather, forecast = wf
    windspeed = round((weather['wind']['speed'] * 3.6 / 3) ** (2 / 3))
    winddir = '89632147'[floor(((weather['wind']['deg'] + 22.5) % 360) / 45)] if 'deg' in weather['wind'] else '5'
    return {
        'R': ceil(sum([w['rain']['3h'] for w in forecast if 'rain' in w and w['rain']])),
        'D': weather['weather'][0]['description'],
        'T': round(weather['main']['temp']),
        'W': '%i%s' % (windspeed, winddir),
    }


def get_next_sunrise_or_sunset(lat, lng):
    now = TZ.localize(datetime.now())
    dt = cache.get('pebble_sun')
    if dt is None or dt > now:
        r = requests.get('http://api.sunrise-sunset.org/json', {'lat': lat, 'lng': lng})
        if r.status_code != 200:
            return {}

        def get_datetime(results):
            today = date.today().strftime('%Y/%m/%d ')
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            dt = datetime.strptime(today + r.json()['results'][results], '%Y/%m/%d %I:%M:%S %p')
            locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
            return utc.localize(dt).astimezone(TZ)

        sunrise = get_datetime('sunrise')
        sunset = get_datetime('sunset')
        dt = sunset if sunrise < now < sunset else sunrise
        cache.set('pebble_sun', dt, 900)
    return {'H': dt.hour, 'M': dt.minute}


def get_calendar():
    calendar = [item[:24].strip()
                for item in check_output('khal list', shell=True).decode().split('\n')
                if item and 'Today' not in item:
                ]
    return {'C%i' % i: it for i, it in enumerate(calendar)}


def pebble(request, lon=None, lat=None):
    if lon is None:
        lat, lon = cache.get('pebble_pos', TOULOUSE)
    else:
        cache.set('pebble_pos', (lat, lon), 3600 * 24)

    rep = get_calendar()
    rep.update(get_weather(lat, lon))
    rep.update(get_next_sunrise_or_sunset(lat, lon))

    return JsonResponse(rep)
