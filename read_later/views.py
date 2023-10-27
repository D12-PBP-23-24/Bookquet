from django.shortcuts import render,redirect,HttpResponseRedirect,get_object_or_404
from main.models import Book
from read_later.models import ReadLaterBooks
from django.contrib.auth.decorators import login_required
from .forms import AddToReadLaterForm
from django.http import JsonResponse,HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib import messages  
import json

# def all_list(request):
#     books = Book.objects.all()
#     return render(request, 'list.html', {"books":books})

# def read_later_list(request):
#     entries = ReadLaterBooks.objects.all()
#     return render(request, 'read_later_list.html', {'entries': entries})

# def add_to_read_later(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#     ReadLaterBooks.objects.get_or_create(book=book)
#     print(ReadLaterBooks.id)
#     print(ReadLaterBooks.objects.count())
#     return redirect('read_later:read_later_list')

# def remove_from_read_later(request, read_later_id):
#     read_later_entry = get_object_or_404(ReadLaterBooks, id=read_later_id)
#     read_later_entry.delete()
#     return redirect('read_later:read_later_list')


@login_required
def all_list(request):
    books = Book.objects.all()
    return render(request, 'list.html', {"books":books})

# @login_required
# def read_later_list(request):
#     print("fa")
#     entries = ReadLaterBooks.objects.filter(user=request.user)
#     return render(request, 'read_later_list.html', {'entries': entries})
#     # return HttpResponse(serializers.serialize('json', entries))

# @login_required
# def read_later_list2(request,priority = "all"):
#     print("faf")
#     if(priority == "all"):
#         entries = ReadLaterBooks.objects.filter(user=request.user)
#     else:
#         entries = ReadLaterBooks.objects.filter(user=request.user).filter(priority = priority)
#     return render(request, 'read_later_list.html', {'entries': entries})
#     # return HttpResponse(serializers.serialize('json', entries))

@login_required
def read_later_list_json(request):
    priority = request.GET.get("priority", "all")
    if(priority == "all"):
        entries = ReadLaterBooks.objects.filter(user=request.user).select_related("book")
    else:
        entries = ReadLaterBooks.objects.filter(user=request.user).filter(priority = priority).select_related("book")
    list = []
    for row in entries:
            list.append({
                'id': row.pk,
                'title': row.book.title,
                'author': row.book.author,
                'description': row.book.description,
                'isbn': row.book.isbn,
                'genres': row.book.genres,
                'cover_img': row.book.cover_img,
                'year': row.book.year
            })
    return HttpResponse(json.dumps(list), content_type="application/json")
    # return HttpResponse(serializers.serialize('json', entries))

@login_required
def read_later_list(request):
    priority = request.GET.get("priority", "all")
    if(priority == "all"):
        entries = ReadLaterBooks.objects.filter(user=request.user)
    else:
        entries = ReadLaterBooks.objects.filter(user=request.user).filter(priority = priority)
    return render(request, "read_later_list2.html", context={"entries": entries})

@login_required
def add_to_read_later(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    data = {'success': False}
    if request.method == 'POST':
        form = AddToReadLaterForm(request.POST)
        if form.is_valid():
            # priority = form.cleaned_data['priority']
            priority = request.POST.get('priority')
            ReadLaterBooks.objects.get_or_create(user=request.user, book=book, priority=priority)
            # return redirect(reverse('read_later:read_later_list'))
            data['success'] = True
            data['redirect_url'] = reverse('read_later:read_later_list')
            return JsonResponse(data)
        else:
            
            data['error'] = 'Invalid form data.'
            return JsonResponse(data, status=400)
    else:
        form = AddToReadLaterForm()

    context = {
        'form': form,
        'book': book
    }
    return render(request, 'add_to_read_later_form.html', context)

# @login_required
# def remove_from_read_later(request, entry_id):
#     # Retrieve the relevant entry
#     entry = get_object_or_404(ReadLaterBooks, id=entry_id, user=request.user)

#     # Delete the entry
#     entry.delete()

#     # Redirect back to the read later list
#     return HttpResponseRedirect(reverse('read_later:read_later_list', args=('all',)))

@csrf_exempt
@login_required
def delete_item_ajax(request, item_id):
    if request.method == 'DELETE':
        item = ReadLaterBooks.objects.get(id=item_id)
        item.delete()
        return HttpResponse({'status': 'DELETED'}, status=200)
    
# @login_required
# def remove_from_read_later(request, read_later_id):
#     read_later_entry = get_object_or_404(ReadLaterBooks, id=read_later_id)
#     if read_later_entry.user != request.user:
#         return JsonResponse({'success': False, 'message': 'Permission Denied'})

#     read_later_entry.delete()
#     return JsonResponse({'success': True})


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('read_later:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("read_later:all_list")) 
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
