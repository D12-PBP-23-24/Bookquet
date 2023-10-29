from django.shortcuts               import render, redirect
from django.http                    import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf   import csrf_exempt
from django.contrib.auth.decorators import login_required

from main.models        import Book, UserProfile
from main.forms         import UserProfileForm, AddBookForm
from .models            import QuoteOfDay
from .forms             import QuoteOfDayForm

@csrf_exempt
def show_dashboard(request):
    user = request.user  # Mengambil objek pengguna yang sedang masuk
    profile = UserProfile.objects.get(username=user.username)  

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, "dashboard.html", context)

@login_required
def manage_quote_of_the_day(request):
    quote = QuoteOfDay.objects.first()
    if request.method == 'POST':
        form = QuoteOfDayForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
    else:
        form = QuoteOfDayForm(instance=quote)

    return render(request, 'manage_quote.html', {'form': form})

@login_required
def edit_quote_of_the_day(request):
    # Ambil objek Quote of the Day yang ada
    quote_of_the_day = QuoteOfDay.objects.first()

    if not request.user.is_staff:
        return redirect('adminpage:show_main')  # Redirect jika bukan admin

    if request.method == 'POST':
        form = QuoteOfDayForm(request.POST, instance=quote_of_the_day)
        if form.is_valid():
            form.save()
            return redirect('adminpage:show_main') 
    else:
        form = QuoteOfDayForm(instance=quote_of_the_day)

    context = {'form': form, 'quote_of_the_day': quote_of_the_day}
    return render(request, 'edit_quote.html', context)

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
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'})
        else:
            errors = form.errors
            return JsonResponse({'status': 'error', 'message': "Terjadi kesalahan saat edit profile ", 'errors': errors})
    else:
        return HttpResponseBadRequest("Invalid Request Method")
        