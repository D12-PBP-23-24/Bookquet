from django.shortcuts import render
from django.http import HttpResponseRedirect
from dashboard.forms import BookForm, ProfileForm
from django.urls import reverse
from dashboard.models import Book, Profile
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
# from main.forms import ItemForm
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import datetime
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def show_dashboard(request):

    user = request.user  # Mengambil objek pengguna yang sedang masuk
    # profile = Profile.objects.get(user=user)  
    # nickname = profile.nickname
    # age = profile.age
    # phone = profile.phone

    context = {
        'username': user.username,
        'class': 'PBP',
        # 'nickname': nickname,
        # 'age': age,
        # 'phone': phone,
        # 'region': region,

    }
    return render(request, "dashboard.html", context)

@csrf_exempt
def get_profile_json(request):
    profile = Profile.objects.get(user=request.user)
    profile_data = {
        'nickname': profile.nickname,
        'username': profile.username,
        'age': profile.age,
        'phone': profile.phone,
        'region': profile.region,
    }
    return JsonResponse(profile_data)

# @csrf_exempt
# def edit_profile_ajax(request):
#     if request.method == 'POST':
#         user = request.user  # Ambil objek pengguna yang ingin diedit
#         profile = Profile.objects.get(user=user)
#         form = ProfileForm(request.POST, instance=profile)  # Isi formulir dengan data profil pengguna
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'message': 'Profile updated successfully'})
#         else:
#             errors = form.errors
#             return JsonResponse(errors, status=400)
#     else:
#         return HttpResponseBadRequest("Invalid Request Method")


def edit_profile_ajax(request):
    if request.method == 'POST':
        user = request.user
        profile = Profile.objects.get(user=user)
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            updated_profile = form.save()
            return JsonResponse({'message': 'Profile updated successfully', 'profile': updated_profile})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'errors': errors}, status=400)
    else:
        return HttpResponseBadRequest("Invalid Request Method")
        


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('dashboard:login')
    context = {'form':form}
    return render(request, 'register.html', context)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("dashboard:show_dashboard")) 
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