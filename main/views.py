from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from main.models import Book
from main.forms import AddBookForm

def show_main(request):
    form = AddBookForm(request.POST or None)
    books = Book.objects.all()
    context = {
        'books': books,
        'form': form
    }
    return render(request, "main.html", context)

def get_books(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_book_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data))

@csrf_exempt
def find_book(request):
    books = Book.objects.all().values()

    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title", "")
        genre = data.get("genre", "All")

        if genre == "All":
            books = Book.objects.filter(title__icontains=title).values()
        else:
            books = Book.objects.filter(title__icontains=title, genres=genre).values()   

    return JsonResponse({'books': list(books)})
