from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserProfileForm(UserCreationForm):
    nickname = forms.CharField(required=True)
    phone = forms.IntegerField(required=True)
    age = forms.IntegerField(required=True)
    region = forms.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'password2', 'nickname', 'phone', 'age', 'region')
