from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse

from main.models import Book

def show_main(request):
    books = Book.objects.all()
    context = {
        'books': books, 
    }
    return render(request, "main.html", context)

def get_books(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_book_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data))