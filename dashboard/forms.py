from django.forms import ModelForm
from main.models import Book, UserProfile

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nickname", "age", "phone", "region"]