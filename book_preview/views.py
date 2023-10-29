from django.shortcuts import render
from main.models import Book
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from book_preview.models import Comment, Rate
from .forms import RateForm, CommentForm
from .utils import calculate_new_average_rating
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
import json
from django.http import JsonResponse
from django.core import serializers

def show_preview(request, book_id):
    book = Book.objects.get(pk = book_id)
    rate = Rate.objects.filter(buku = book)
    comment = Comment.objects.filter(buku = book)
    
    context = {
        "book": book,
        "rate": rate,
        "average_rate_floored": book.average_rate//1, #due to lack of flexibility from django template if-else statement
        "comment": comment
    }
    return render(request, "preview.html", context)

def add_rating_comment(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    data = {'success': False}

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        rate_form = RateForm(request.POST)

        if comment_form.is_valid() and rate_form.is_valid():
            user = request.user
            rating = rate_form.cleaned_data['rating']
            komentar = comment_form.cleaned_data['komentar']

            existing_rating = Rate.objects.filter(buku=book, user=user).first()
            existing_komentar = Comment.objects.filter(buku=book, user=user).first()

            if existing_rating:
                existing_rating.rating = rating
                existing_komentar.komentar = komentar
                existing_rating.save()
                existing_komentar.save()
            else:
                Rate.objects.create(buku=book, user=user, rating=rating)
                Comment.objects.create(buku=book, user=user, komentar=komentar)

            new_average = calculate_new_average_rating(book)

            book.average_rate = new_average
            book.user_rated = Rate.objects.filter(buku=book).count()
            book.save()

            data['success'] = True
            data['redirect_url'] = reverse('book_preview:show_preview', args=[book.id])
            return JsonResponse(data)

        else:
            errors = {
                'comment_errors': comment_form.errors,
                'rate_errors': rate_form.errors
            }
            data['errors'] = errors
            return JsonResponse(data, status=400)
    else:
        comment_form = CommentForm()
        rate_form = RateForm()

    context = {
        'book': book,
        'comment_form': comment_form,
        'rate_form': rate_form,
    }

    return render(request, 'rate_review.html', context)

@login_required
def recomendation_book(request, book_id):
    filter = request.GET.get("filter", "genre")
    book = Book.objects.get(pk=book_id)

    if filter == "genre":
        book_genres = book.genres
        entries = Book.objects.filter(genres=book_genres).exclude(pk=book.pk)
    else:
        entries = Book.objects.filter(average_rate__gte=4).exclude(pk=book.pk)

    entries_data = serializers.serialize("json", entries)
    
    list = []
    for row in entries:
            list.append({
                'id': row.pk,
                'title': row.title,
                'author': row.author,
                'description': row.description,
                'isbn': row.isbn,
                'genres': row.genres,
                'cover_img': row.cover_img,
                'year': row.year,
                'average_rate': row.average_rate,
                'user_rated': row.user_rated
            })
    return HttpResponse(json.dumps(list), content_type="application/json")

    # Return the serialized data as a JSON response
    return JsonResponse(entries_data, safe=False)




