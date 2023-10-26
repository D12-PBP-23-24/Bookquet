from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from adminpage.forms import BookForm
from django.urls import reverse

from main.models import Book

def show_main(request):
    books = Book.objects.all()
    context = {
        'books': books, 
    }
    return render(request, "main.html", context)

def add_book(request):
    form =  BookForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('adminpage:show_main'))

    context = {'form': form}
    return render(request, "add_book.html", context)

def show_xml(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Book.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Book.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

#def get_books(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

#def get_book_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data))


