from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from .models import Supervisor, User


class SupervisorAdminForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super(SupervisorAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email

    class Meta:
        model = Supervisor
        fields = "__all__"

    def save(self, commit=True):
        supervisor = super().save(commit=False)

        if self.instance.pk is None:
            user_data = {
                'username': self.cleaned_data['username'],
                'email': self.cleaned_data['email'],
                'password': self.cleaned_data['password'],
            }
            user = User.objects.create_user(**user_data)
            supervisor.user = user
        else:
            user = supervisor.user
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data['email']
            if self.cleaned_data['password']:
                user.set_password(self.cleaned_data['password'])
            user.save()

        supervisor_group, _ = Group.objects.get_or_create(name='supervisors')
        user.groups.add(supervisor_group)

        if commit:
            supervisor.save()
        return supervisor


class SupervisorAdmin(admin.ModelAdmin):
    form = SupervisorAdminForm
    readonly_fields = ['user']
    list_display = ['user', "get_email"]

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = "email"

admin.site.register(Supervisor, SupervisorAdmin)
admin.site.register(User)
