from datetime import datetime, date
import locale
from math import ceil, floor
from subprocess import check_output

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.views.decorators.cache import cache_page


from braces.views import SuperuserRequiredMixin
from photologue.models import Gallery, Photo
from pytz import timezone, utc
import requests

from .forms import UserForm
from .models import Position

DATE_FMT = '%Y/%m/%d '
TIME_FMT = '%I:%M:%S %p'
DT_FMT = DATE_FMT + TIME_FMT


@login_required
def profil(request):
    if request.method == 'POST':
        if 'username' in request.POST:
            form = UserForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profil mis à jour")
        else:
            if request.user.check_password(request.POST['old_password']):
                if request.POST['new_password1'] == request.POST['new_password2']:
                    request.user.set_password(request.POST['new_password1'])
                    request.user.save()
                    messages.success(request, "Mot de passe mis à jour")
                else:
                    messages.error(request, "Les deux mots de passe entrés ne concordent pas")
            else:
                messages.error(request, "Mauvais «Ancien mot de passe»")
    return render(request, 'profil.html', {
        'form': UserForm(instance=request.user),
        'pwform': PasswordChangeForm(request.user),
    })


class PhotoDetailView(SuperuserRequiredMixin, DetailView):
    model = Photo


class GalleryPhotoDetailView(DetailView):
    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        self.gallery = get_object_or_404(Gallery, slug=slug)
        self.index = int(self.kwargs.get('index', 1))
        self.max_index = self.gallery.photos.count()

        if not 0 < self.index <= self.max_index:
            raise Http404

        return self.gallery.photos.all()[self.index - 1]

    def get_context_data(self, **kwargs):
        c = {'gallery': self.gallery, 'index': self.index}
        if self.index > 1:
            c['prev'] = self.gallery.photos.all()[self.index - 2]
        if self.index < self.max_index:
            c['next'] = self.gallery.photos.all()[self.index]
        return super(GalleryPhotoDetailView, self).get_context_data(**c)


# @cache_page(60 * 15)
def pebble(request, lon=None, lat=None):
    # TODO: app

    if lon is None:
        last = Position.objects.last()
        lon, lat = last.lon, last.lat
    else:
        Position.objects.create(lon=lon, lat=lat)

    calendar = [item[:24].strip() for item in check_output('khal agenda', shell=True).decode().split('\n')[1:] if item]
    rep = {'C%i' % i: it for i, it in enumerate(calendar)}

    weather = requests.get('http://api.openweathermap.org/data/2.5/forecast',
                           {'units': 'metric', 'lang': 'fr', 'lat': lat, 'lon': lon, 'appid': settings.OWM_KEY,
                            'cnt': round((24 - datetime.now().hour) / 3)})
    weather.raise_for_status()
    weatherl = weather.json()['list']
    rep.update(T=round(weatherl[0]['main']['temp']), D=weatherl[0]['weather'][0]['description'],
               W='%i%s' % (round((weatherl[0]['wind']['speed'] * 3.6 / 3) ** (2 / 3)),
                           '89632147'[floor(((weatherl[0]['wind']['deg'] + 22.5) % 360) / 45)]),
               R=ceil(sum([w['rain']['3h'] for w in weatherl if 'rain' in w and w['rain']])))

    r = requests.get('http://api.sunrise-sunset.org/json', {'lat': lat, 'lng': lon})
    r.raise_for_status()
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    sunrise = datetime.strptime(date.today().strftime(DATE_FMT) + r.json()['results']['sunrise'], DT_FMT)
    sunset = datetime.strptime(date.today().strftime(DATE_FMT) + r.json()['results']['sunset'], DT_FMT)
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    dt = sunset if sunrise < datetime.utcnow() < sunset else sunrise
    dt = utc.localize(dt).astimezone(timezone('Europe/Paris'))
    rep.update(H=dt.hour, M=dt.minute)

    return JsonResponse(rep)
