from django import forms
from .models import ReadLaterBooks

class AddToReadLaterForm(forms.ModelForm):
    class Meta:
        model = ReadLaterBooks
        fields = ['priority']
