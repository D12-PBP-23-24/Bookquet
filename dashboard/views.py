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
        'phone': profile.phone,
        'region': profile.region,
    }
    return JsonResponse(profile_data)

# @csrf_exempt
# def get_profile_json(request):
#     profiles = Profile.objects.filter(user=request.user)
#     prof_list = []
#     for prof in profiles:
#         prof_dict = {
#             'nickname': prof.nickname,
#             'username': prof.username,
#             'age': prof.age,
#             'phone': prof.phone,
#             'region': prof.region,
#         }
#         prof_list.append(prof_dict)
#     return JsonResponse(prof_list, safe=False)

# ...
# @csrf_exempt
# def edit_profile_ajax(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST)

#         if form.is_valid():
#             prof = form.save(commit=False)
#             prof.user = request.user
#             prof.save()
#             return HttpResponse("Created", status=201)
#         else:
#             # Handle form validation errors and return as JSON
#             errors = form.errors.as_json()
#             return HttpResponseBadRequest(errors, content_type='application/json')

#     return HttpResponseNotFound()

...
@csrf_exempt
def edit_profile_ajax(request):
    user = request.user  #ambil objek pengguna yang ingin diedit
    profile = Profile.objects.get(user=user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)  #isi formulir dengan data profil pengguna
        print(formj)
        if form.is_valid():
            form.save() 
            return JsonResponse({'message': 'Profile updated successfully'})
        else:
            errors = form.errors
            return JsonResponse(errors, status=400)
        
