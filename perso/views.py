from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView


from braces.views import SuperuserRequiredMixin
from photologue.models import Gallery, Photo

from .forms import UserForm


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
