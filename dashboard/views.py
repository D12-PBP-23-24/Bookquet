from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from main.models import Book, UserProfile
from .forms import ProfileForm
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from django.core import serializers

@csrf_exempt
def show_dashboard(request):
    # books_reviewed = Book.objects.filter(user_rated=request.user)

    user = request.user  # Mengambil objek pengguna yang sedang masuk
    profile = UserProfile.objects.get(username=user.username)  

    context = {
        'user': user,
        'profile': profile,
        # 'books_reviewed' : books_reviewed,
        # 'nickname': nickname,
        # 'age': age,
        # 'phone': phone,

    }
    return render(request, "dashboard.html", context)


@csrf_exempt
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
