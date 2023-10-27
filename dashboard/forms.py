from django.forms import ModelForm
from dashboard.models import Book, Profile

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "description", "publish_date"]

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["nickname", "username", "age", "phone", "region"]