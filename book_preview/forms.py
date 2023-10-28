from main.models import Book
from book_preview.models import Comment

from django.forms import ModelForm
from .models import Comment, Rate

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['komentar']

class RateForm(ModelForm):
    class Meta:
        model = Rate
        fields = ['rating']