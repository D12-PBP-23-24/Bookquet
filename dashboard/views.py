from django.shortcuts import render

from main.models import Book, UserProfile
from .forms import ProfileForm
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core import serializers

from book_preview.models import Rate
from book_preview.models import Comment

@login_required
def show_dashboard(request):
    user = request.user 
    profile = UserProfile.objects.get(username=user.username)  
    rated_books = get_rated_books_for_user(user)
    commented_books = get_commented_books_for_user(user)

    context = {
        'user': user,
        'profile': profile,
        'rated_books': rated_books,
        'commented_books': commented_books,
    }
    return render(request, "dashboard.html", context)

def get_rated_books_json(request):
    user = request.user
    rated_books = Rate.objects.filter(user=user).values_list('buku', flat=True)
    rated_books = Book.objects.filter(pk__in=rated_books)
    rated_books_data = [
        {
            "title": book.title,
            "author": book.author,
            "cover_img": book.cover_img,
            "genres": book.genres,
        }
        for book in rated_books
    ]
    return JsonResponse(rated_books_data, safe=False)

def get_profile_json(request):
    user = request.user
    profile = UserProfile.objects.get(username=user.username)
    profile_data = {
        'nickname': profile.nickname,
        'username': profile.username,
        'age': profile.age,
        'phone': profile.phone,
        'region': profile.region,
    }
    return JsonResponse(profile_data)



def filter_books_view(request):
    filter_param = request.GET.get("filter")
    user = request.user

    if filter_param == "all":
        rated_books = Rate.objects.filter(user=user).values_list('buku', flat=True)
        books = Book.objects.filter(pk__in=rated_books)
    else:
        rated_books = Rate.objects.filter(user=user, rating=filter_param).values_list('buku', flat=True)
        books = Book.objects.filter(pk__in=rated_books)

    books_data = [
        {
            "id" : book.pk,
            "title": book.title,
            "author": book.author,
            "cover_img": book.cover_img,
            "genres": book.genres,
            "rating": filter_param, 
        }
        for book in books
    ]

    return JsonResponse(books_data, safe=False)

def get_rated_books_for_user(user):
    rated_books = Rate.objects.filter(user=user).values_list('buku', flat=True)
    return Book.objects.filter(pk__in=rated_books)

def get_commented_books_for_user(user):
    commented_books = Comment.objects.filter(user=user).values_list('buku', flat=True)
    return Book.objects.filter(pk__in=commented_books)

@csrf_exempt
def edit_profile_ajax(request):
    if request.method == 'POST':
        user = request.user
        profile = UserProfile.objects.get(username=user.username)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})
        else:
            errors = form.errors
            return JsonResponse({'status': 'error', 'message': "Terjadi kesalahan saat edit profile ", 'errors': errors})
    else:
        return HttpResponseBadRequest("Invalid Request Method")
    
def show_xml(request):
    data = UserProfile.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = UserProfile.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
