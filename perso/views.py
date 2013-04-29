#-*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render


def login_view(request):
    if request.method == 'GET':
        c = {}
        if 'next' in request.GET:
            c['next'] = request.GET['next']
        return render(request, 'home.html', c)
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            if user.is_superuser:
                messages.set_level(request, messages.DEBUG)
            messages.success(request, u"Vous avez été authentifié avec succès")
            messages.debug(request, u"Debug on for surperadmin")
        else:
            messages.error(request, u"Votre compte utilisateur a été désactivé…")
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
    messages.info(request, u"Vous avec été déconnecté avec succès")
    return redirect('/')


def about(request):
    return redirect('/')  # TODO

def home(request):
    return render(request, 'home.html', {})
