from subprocess import check_output

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView

from braces.views import SuperuserRequiredMixin
from photologue.models import Gallery, Photo
import requests

from .models import UserForm


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


def pebble(request, lon, lat):
    # TODO: app, key

    calendar = [item[:25] for item in check_output('khal agenda', shell=True).decode().split('\n')[1:] if item]
    weather = requests.get('http://api.openweathermap.org/data/2.5/weather',
                           {'units': 'metric', 'lang': 'fr', 'lat': lat, 'lon': lon, 'appid': settings.OWM_KEY})
    weather.raise_for_status()

    def wind_force(wind_speed):
        return round((wind_speed * 3.6 / 3) ** (2 / 3))

    def wind_dir(wind):
        if wind <= 11.25:
            return ' ↑ '
        if wind <= 33.75:
            return 'NNE'
        if wind <= 56.25:
            return ' ↗ '
        if wind <= 78.75:
            return 'ENE'
        if wind <= 101.25:
            return ' → '
        if wind <= 123.75:
            return 'ESE'
        if wind <= 146.25:
            return ' ↘ '
        if wind <= 168.75:
            return 'SSE'
        if wind <= 191.25:
            return ' ↓ '
        if wind <= 213.75:
            return 'SSW'
        if wind <= 236.25:
            return ' ↙ '
        if wind <= 258.75:
            return 'WSW'
        if wind <= 281.25:
            return ' ← '
        if wind <= 303.75:
            return 'WNW'
        if wind <= 326.25:
            return ' ↖ '
        if wind <= 348.75:
            return 'NNW'
        return ' ↑ '

    weather = weather.json()
    return JsonResponse({'CALENDAR': calendar, 'TEMPERATURE': weather['main']['temp'],
                         'CONDITIONS': weather['weather'][0]['description'],
                         'WIND': wind_force(weather['wind']['speed']),
                         'WINDDIR': wind_dir(weather['wind']['deg']),
                         })
