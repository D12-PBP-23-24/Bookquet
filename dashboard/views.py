from django.shortcuts import render
from django.http import HttpResponseRedirect
from dashboard.forms import BookForm, ProfileForm
from django.urls import reverse
from dashboard.models import Book, Profile
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

def show_main(request):
    context = {
        'name': request.user.username,
        'class': 'PBP',
    }
    return render(request, "dashboard.html", context)

@csrf_exempt
def get_profile_json(request):
    profile = Profile.objects.get(user=request.user)
    profile_data = {
        'nickname': profile.nickname,
        'username': profile.username,
        'age': profile.age,
        'phonenumber': profile.phone,
        'region': profile.region,
    }
    return JsonResponse(profile_data)

...
@csrf_exempt
def edit_profile_ajax(request):
    user = request.user  #ambil objek pengguna yang ingin diedit
    profile = Profile.objects.get(user=user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)  #isi formulir dengan data profil pengguna
        if form.is_valid():
            form.save() 
            return JsonResponse({'message': 'Profile updated successfully'})
        else:
            errors = form.errors
            return JsonResponse(errors, status=400)
        
