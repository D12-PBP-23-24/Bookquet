from django import forms
from .models import Book

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'genres']

    GENRE_CHOICES = (
        ('All', 'All'),
        ('Young Adult', 'Young Adult'),
        ('Fantasy', 'Fantasy'),
        ('Classics', 'Classics'),
        ('Historical Fiction', 'Historical Fiction'),
        ('Childrens', 'Childrens'),
        ('Fiction', 'Fiction'),
        ('Science Fiction', 'Science Fiction'),
        ('Horror', 'Horror'),
        ('Nonfiction', 'Nonfiction'),
        ('Romance', 'Romance'),
        ('Mystery', 'Mystery'),
        ('Picture Books', 'Picture Books'),
    )

    title  = forms.CharField(widget = forms.TextInput( attrs = { 'class': 'form-control', }), required = False)
    genres = forms.ChoiceField(widget = forms.Select( attrs = { 'class': 'form-control', }), choices = GENRE_CHOICES, required = True)