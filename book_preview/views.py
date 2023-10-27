from django.shortcuts import render
from main.models import Book
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from book_preview.models import Comment, Rate
from django.http import JsonResponse
# from book_preview.forms import ReviewBookForm
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import RateForm, CommentForm

def show_preview(request, book_id):
    book = Book.objects.get(pk = book_id)
    rate = Rate.objects.filter(buku = book)
    
    context = {
        "book": book,
        "rate": rate
    }
    return render(request, "preview.html", context)

def add_rating_comment(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    data = {'success': False}

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        rate_form = RateForm(request.POST)

        if comment_form.is_valid() and rate_form.is_valid():
            # Handle form data
            return JsonResponse({'success': True})
        else:
            errors = {
                'comment_errors': comment_form.errors,
                'rate_errors': rate_form.errors
            }
            return JsonResponse({'success': False, 'errors': errors})
    
    else:
        comment_form = CommentForm()
        rate_form = RateForm()

        context = {
            'book': book,
            'comment_form': comment_form,
            'rate_form': rate_form,
        }

        return render(request, 'rate_review.html', context)
