# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from braces.views import SuperuserRequiredMixin

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView
from photologue.models import Gallery, Photo

from .models import User, UserForm


def login_view(request):
    if request.method == 'GET':
        messages.error(request, 'Vous n’êtes pas loggé')
        next = '/'
        if 'next' in request.GET:
            next += '?next=%s' % request.GET['next']
        return redirect(next)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            if user.is_superuser:
                messages.set_level(request, messages.DEBUG)
            messages.success(request, "Vous avez été authentifié avec succès")
            messages.debug(request, "Debug on for surperadmin")
        else:
            messages.error(request, "Votre compte utilisateur a été désactivé…")
    else:
        messages.error(request, "Les identifiants entrés sont incorrects.")
    next = '/'
    if 'next' in request.POST:
        next = request.POST['next']
    if 'next' in request.GET:
        next = request.GET['next']
    return redirect(next)


def logout_view(request):
    logout(request)
    messages.info(request, "Vous avec été déconnecté avec succès")
    return redirect('/')


@login_required
def profil(request):
    form = UserForm(instance=request.user)
    c = {}
    if request.method == 'POST':
        if 'old_username' in request.POST:
            form = UserForm(request.POST, instance=request.user)
            if form.is_valid():
                updated_user = User.objects.get(username=request.POST['old_username'])
                if updated_user == request.user:
                    form.save()
                    messages.success(request, "Profil mis à jour")
                else:
                    messages.error(request, "NAMÉHO, c’est pas ton profil ça !")
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
    c['form'] = form
    c['pwform'] = PasswordChangeForm(request.user)
    return render(request, 'profil.html', c)


def rsssub_view(request, url):
    return HttpResponse(url, content_type="text/plain")


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
