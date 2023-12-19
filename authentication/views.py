from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.forms import UserProfileForm
from main.models import Book
from django.http import HttpResponse
from django.core import serializers
from main.models import UserProfile
import json

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            return JsonResponse({
                "username": user.username,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)

def show_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout success!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout failed"
        }, status=401)
    
@csrf_exempt
def register(request):
    if request.method == "POST":
        input_data = json.loads(request.body)
        print(input_data)
        username = input_data.get('username')
        password = input_data.get('password')
        password_confirmation = input_data.get('confirmPassword')
        nickname = input_data.get('nickname')
        phone = input_data.get('phone')
        age = input_data.get('age')
        region = input_data.get('region')

        if password != password_confirmation:
            return JsonResponse({
                "status": "Gagal",
                "message": "Password tidak sama."
            }, status=401)

        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Assuming UserProfile is your model for additional fields
        user_profile = UserProfile.objects.create(
            user=user,
            nickname=nickname,
            phone=int(phone),
            age=int(age),
            region=region
        )
        user_profile.save()

        return JsonResponse({
            "status": "Berhasil",
            "message": "Register berhasil!"
        }, status=200)

    return JsonResponse({
        "status": "Gagal",
        "message": "Register gagal."
    }, status=401)