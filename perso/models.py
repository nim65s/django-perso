from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['last_login'].widget.attrs['readonly'] = True
            self.fields['date_joined'].widget.attrs['readonly'] = True

    def clean_last_login(self):
        return self.instance.last_login

    def clean_date_joined(self):
        return self.instance.date_joined
