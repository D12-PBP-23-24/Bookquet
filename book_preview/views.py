from django.shortcuts import render
from main.models import Book
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from book_preview.models import Comment, Rate, Filter
from .forms import RateForm, CommentForm
from .utils import calculate_new_average_rating
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
import json
from django.http import JsonResponse
from django.core import serializers
from random import sample


def show_preview(request, book_id):
    book = Book.objects.get(pk = book_id)
    rate = Rate.objects.filter(buku = book)
    comment = Comment.objects.filter(buku = book)

    try:
        global_filter = Filter.objects.first()
        if global_filter is not None:
            default_filter = global_filter.filter_type
        else:
            default_filter = 'terbaru'
    except Filter.DoesNotExist:
        default_filter = 'terbaru'
    
    context = {
        "book": book,
        "rate": rate,
        "average_rate_floored": book.average_rate//1, #due to lack of flexibility from django template if-else statement
        "comment": comment,
        "default_filter": default_filter,
    }

    return render(request, "preview.html", context)

@login_required
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


def filter_comments(request, filter_type):
    # Handle the filter logic
    if filter_type == 'recent':
        comments = Comment.objects.order_by('-id')[:2]  # Get the 6 most recent comments
    elif filter_type == 'random':
        all_comments = Comment.objects.all()
        if all_comments.count() <= 2:
            comments = all_comments  # If there are 6 or fewer comments, no need to sample
        else:
            random_comments = sample(list(all_comments), 2)  # Sample 6 random comments
            comments = Comment.objects.filter(id__in=[c.id for c in random_comments])
    
    print(comments)

    comment_data = [
        {
            'komentar': comment.komentar,
            'book_title': comment.buku.title,
            'user': comment.user.username
        }
        for comment in comments
    ]

    return JsonResponse({'comments': comment_data})


def update_global_filter_settings(request):
    if request.user.is_staff:
        # Check if the user is an admin (staff member)
        try:
            global_filter = Filter.objects.first()
            if global_filter is not None:
                # Update the filter type based on the request data
                filter_type = request.GET.get('filter_type')
                global_filter.filter_type = filter_type
                global_filter.save()
                return JsonResponse({'success': True})
            else:
                # Create a new global filter if it doesn't exist
                filter_type = request.GET.get('filter_type', 'terbaru')
                Filter.objects.create(filter_type=filter_type)
                return JsonResponse({'success': True})
        except Filter.DoesNotExist:
            # Handle the case where no Filter object exists
            return JsonResponse({'success': False, 'error': 'Filter does not exist'})
    else:
        # Handle the case where a non-admin user is trying to update the filter (optional)
        return JsonResponse({'success': False, 'error': 'Permission denied'})
