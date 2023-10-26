from django.shortcuts import render
from main.models import Book

def show_preview(request, id):
    book = Book.objects.get(pk = id)
    
    context = {
        "book": book
    }

    print(book.title)
    return render(request, "preview.html", context)
