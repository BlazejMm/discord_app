from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Channel


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self._build_email(user.username)
        if commit:
            user.save()
        return user

    def _build_email(self, username):
        User = get_user_model()
        base = username.lower().replace(" ", "")
        email = f"{base}@komunikator.local"
        counter = 1
        while User.objects.filter(email=email).exists():
            email = f"{base}{counter}@komunikator.local"
            counter += 1
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("avatar_url", "bio")
        labels = {
            "avatar_url": "Link do avatara",
            "bio": "Opis",
        }
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ("name",)
        labels = {"name": "Nazwa przestrzeni"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control"})
