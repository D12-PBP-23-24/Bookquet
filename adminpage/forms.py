from django import forms
from django.contrib.auth.forms import UserCreationForm
from main.models import UserProfile, QuoteOfDay

class UserProfileForm(UserCreationForm):
    nickname = forms.CharField(required=True)
    phone = forms.IntegerField(required=True)
    age = forms.IntegerField(required=True)
    region = forms.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'nickname', 'phone', 'age', 'region']

class QuoteOfDayForm(forms.ModelForm):
    class Meta:
        model = QuoteOfDay
        fields = ['quote_text', 'author']
        
        