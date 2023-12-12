# Create your views here.
import json
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
#from django.contrib.auth import register as auth_register
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main.models import Book
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.models import User
from main.models import UserProfile


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
                "message": "Login successful!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed. Account deactivated."
            }, status=500)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login failed, make sure to input the correct email and password."
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
        data = json.loads(request.body)
        print(data)
        username = data['username']
        password = data['password']
        password_confirmation = data['confirmPassword']

        if password != password_confirmation:
            return JsonResponse({
                "status": "Gagal",
                "message": "Password tidak sama."
            }, status=401)

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Register gagal, username sudah digunakan."
            }, status=400)

        # Create new user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Create user profile
        nickname = data['nickname']
        try:
            phone = int(data['phone'])
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "Phone number must be an integer."
            }, status=400)
        try:
            age = int(data['age'])
        except ValueError:
            return JsonResponse({
                "status": False,
                "message": "Age number must be an integer."
            }, status=400)
        region = data['region']
        
        user_profile = UserProfile(user=user, nickname=nickname, phone=phone, age=age, region=region)
        user_profile.save()

        return JsonResponse({
            "status": "Register berhasil!",
            "message": "Register berhasil!"
        }, status=201)

    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request"
        }, status=400)
