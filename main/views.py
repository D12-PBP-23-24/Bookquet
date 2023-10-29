from django.shortcuts               import render, redirect
from django.core                    import serializers
from django.http                    import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls                    import reverse
from django.contrib                 import messages
from django.contrib.auth            import authenticate, login, logout
from django.views.decorators.csrf   import csrf_exempt
from django.contrib.auth.decorators import login_required

import json
import datetime

from main.models        import Book
from main.forms         import UserProfileForm, AddBookForm
from read_later.views   import add_to_read_later
from .models            import QuoteOfDay
from .forms             import QuoteOfDayForm

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

@login_required
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

@login_required
def read_later_book(request, book_id):
    return add_to_read_later(request=request, book_id=book_id)

@login_required
def manage_quote_of_the_day(request):
    quote = QuoteOfDay.objects.first()
    if request.method == 'POST':
        form = QuoteOfDayForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
    else:
        form = QuoteOfDayForm(instance=quote)

    return render(request, 'manage_quote.html', {'form': form})

@login_required
def edit_quote_of_the_day(request):
    # Ambil objek Quote of the Day yang ada
    quote_of_the_day = QuoteOfDay.objects.first()

    if not request.user.is_staff:
        return redirect('main:show_main')  # Redirect jika bukan admin

    if request.method == 'POST':
        form = QuoteOfDayForm(request.POST, instance=quote_of_the_day)
        if form.is_valid():
            form.save()
            return redirect('main:show_main') 
    else:
        form = QuoteOfDayForm(instance=quote_of_the_day)

    context = {'form': form, 'quote_of_the_day': quote_of_the_day}
    return render(request, 'edit_quote.html', context)