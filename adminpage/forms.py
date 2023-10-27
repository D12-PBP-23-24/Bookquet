from django.forms import ModelForm
from adminpage.models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "description", "isbn", "genres", "cover_img", "year", "rate"]