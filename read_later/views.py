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
from django.conf import settings

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

@login_required
def read_later_list(request):
    priority = request.GET.get("priority", "all")
    if(priority == "all"):
        entries = ReadLaterBooks.objects.filter(user=request.user)
    else:
        entries = ReadLaterBooks.objects.filter(user=request.user).filter(priority = priority)

    is_admin = request.user.is_staff
    return render(request, "read_later_list2.html", context={"entries": entries, "is_admin": is_admin, "last_login": request.COOKIES['last_login']})

@login_required
def add_to_read_later(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    data = {'success': False}
    if request.method == 'POST':
        form = AddToReadLaterForm(request.POST)
        if form.is_valid():
            priority = request.POST.get('priority')
            ReadLaterBooks.objects.get_or_create(user=request.user, book=book, priority=priority)
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

@login_required
@csrf_exempt
def add_to_read_later2(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    data = {'success': False}

    if request.method == 'POST':
        # Create or update the ReadLaterBooks entry with a default priority of 'low'
        priority = request.POST.get('priority')
        ReadLaterBooks.objects.get_or_create(user=request.user, book=book, priority=priority)
        return JsonResponse({'status': 'Added'})
        # return JsonResponse(data)
    else:
        data['error'] = 'Invalid request method.'
        return JsonResponse(data, status=405)
    
@csrf_exempt
@login_required
def delete_item_ajax(request, item_id):
    if request.method == 'DELETE':
        print(request.user)
        item = ReadLaterBooks.objects.get(id=item_id)
        item.delete()
        return JsonResponse({'status': 'DELETED'})

@csrf_exempt
@login_required
def adjust_priority_ajax(request, item_id):
    if request.method == 'POST':
        item = ReadLaterBooks.objects.get(id=item_id)
        if item.priority == 'low':
            item.priority = 'medium'
        elif item.priority == 'medium':
            item.priority = 'high'
        elif item.priority == 'high':
            return JsonResponse({'status': 'Not UPDATED'}, status=200)
        item.save()
        return JsonResponse({'status': 'UPDATED'}, status=200)
