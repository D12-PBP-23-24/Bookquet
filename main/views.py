from django.shortcuts               import render, redirect
from django.core                    import serializers
from django.core.serializers        import serialize
from django.http                    import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls                    import reverse
from django.contrib                 import messages
from django.contrib.auth            import authenticate, login, logout
from django.contrib.auth.models     import User
from django.views.decorators.csrf   import csrf_exempt
from django.contrib.auth.decorators import login_required

import json
import datetime

from main.models        import Book, SearchFeatureStatus, UserProfile
from main.forms         import UserProfileForm, AddBookForm
from read_later.views   import add_to_read_later

def show_main(request):
    form = AddBookForm(request.POST or None)
    books = Book.objects.all()

    for book in books:
        book.average_rate = book.average_rate // 1

    status, created = SearchFeatureStatus.objects.get_or_create(id = 1)
    
    context = {
        'books'     : books,
        'form'      : form,
        'name'      : request.user.username,
        'status'    : status.enabled,
    }

    if request.user.is_authenticated:
        context['last_login']  = request.COOKIES['last_login']

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
    logout(request)
    response = HttpResponseRedirect(reverse('main:show_main'))
    response.delete_cookie('last_login')
    return response

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

@login_required
def logout_user(request):
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

@login_required
def read_later_book(request, book_id):
    return add_to_read_later(request=request, book_id=book_id)

@login_required
@csrf_exempt
def toggle_search_feature(request):
    if request.user.is_authenticated and request.user.is_staff:
        # Get the current status or create one if it doesn't exist
        status, created = SearchFeatureStatus.objects.get_or_create(id = 1)

        # Toggle the status
        status.enabled = not status.enabled
        status.save()

        return JsonResponse({'enabled': status.enabled})
    return JsonResponse({'error': 'Not authorized to toggle the feature status'})

@login_required
@csrf_exempt
def toggle_favorite_status(request, book_id):
    if request.method == 'POST':
        book = Book.objects.get(pk=book_id)
        user = request.user

        if user in book.favorites.all():
            book.favorites.remove(user)
            is_favorite = False
        else:
            book.favorites.add(user)
            is_favorite = True

        book.save()

        return JsonResponse({'is_favorite': is_favorite})