# from django.shortcuts import render
# from django.core import serializers
# from django.http import HttpResponse, HttpResponseNotFound
# from django.http import HttpResponseRedirect
# from adminpage.forms import BookForm
# from django.urls import reverse
# from django.views.decorators.csrf import csrf_exempt

# from main.models import Book

# def show_main(request):
#     books = Book.objects.all()
#     context = {
#         'books': books, 
#     }
#     return render(request, "main.html", context)

# def add_book(request):
#     form =  BookForm(request.POST or None)

#     if form.is_valid() and request.method == "POST":
#         form.save()
#         return HttpResponseRedirect(reverse('main:show_main'))
#     context = {'form': form}
#     return render(request, "add_book.html", context)

# def show_xml(request):
#     data = Book.objects.all()
#     return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# def show_json(request):
#     data = Book.objects.all()
#     return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# def show_xml_by_id(request, id):
#     data = Book.objects.filter(pk=id)
#     return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

# def show_json_by_id(request, id):
#     data = Book.objects.filter(pk=id)
#     return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# def edit_book(request, id):
#     # Get product berdasarkan ID
#     books = Book.objects.get(pk = id)

#     # Set product sebagai instance dari form
#     form = BookForm(request.POST or None, instance=books)

#     if form.is_valid() and request.method == "POST":
#         # Simpan form dan kembali ke halaman awal
#         form.save()
#         return HttpResponseRedirect(reverse('main:show_main'))

#     context = {'form': form}
#     return render(request, "edit_book.html", context)

# def delete_book(request, id):
#     # Get data berdasarkan ID
#     books = Book.objects.get(pk = id)
#     # Hapus data
#     books.delete()
#     # Kembali ke halaman awal
#     return HttpResponseRedirect(reverse('main:show_main'))

# def get_book_json(request):
#     data = Book.objects.all()
#     return HttpResponse(serializers.serialize("json", data))

# def get_books(request):
#     data = Book.objects.all()
#     return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# @csrf_exempt
# def add_book_ajax(request):
#     if request.method == 'POST':
#         title = request.POST.get("title")
#         author = request.POST.get("author")
#         description = request.POST.get("description")
#         isbn = request.POST.get("isbn")
#         genres = request.POST.get("genres")
#         cover_img = request.POST.get("cover_img")
#         year = request.POST.get("year")
#         average_rate = request.POST.get("average_rate")
#         user_rated = request.POST.get("user_rated")
#         user = request.user

#         new_book = Book(title=title, author=author, description=description, isbn=isbn, genres=genres, cover_img=cover_img, year=year, average_rate=average_rate, user_rated=user_rated, user=user)
#         new_book.save()

#         return HttpResponse(b"CREATED", status=201)

#     return HttpResponseNotFound()