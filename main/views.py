from django.shortcuts               import render, redirect
from django.core                    import serializers
from django.http                    import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls                    import reverse
from django.contrib                 import messages
from django.contrib.auth            import authenticate, login, logout
from django.views.decorators.csrf   import csrf_exempt

import json
import datetime

from main.models import Book
from main.forms import UserProfileForm, AddBookForm

def show_main(request):
    form = AddBookForm(request.POST or None)
    books = Book.objects.all()
    context = {
        'books': books,
        'form': form,
        'name' : request.user.username,
    }
    return render(request, "main.html", context)

def get_books(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_book_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data))

def register(request):
    form = UserProfileForm()
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    print('test')
    logout(request)
    response = HttpResponseRedirect(reverse('main:show_main'))
    response.delete_cookie('last_login')
    return response

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
