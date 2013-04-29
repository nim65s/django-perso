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
                    messages.success(request, u"Profil mis à jour")
                else:
                    messages.error(request, u"NAMÉHO, c’est pas ton profil ça !")
        else:
            if request.user.check_password(request.POST['oldpw']):
                if request.POST['newpw'] == request.POST['verpw']:
                    request.user.set_password(request.POST['newpw'])
                    request.user.save()
                    messages.success(request, u"Mot de passe mis à jour")
                else:
                    messages.error(request, u"Les deux mots de passe entrés ne concordent pas")
            else:
                messages.error(request, u"Mauvais «Ancien mot de passe»")
    c['form'] = form
    return render(request, 'profil.html', c)


def about(request):
    return redirect('/')  # TODO

def home(request):
    return render(request, 'home.html', {})
