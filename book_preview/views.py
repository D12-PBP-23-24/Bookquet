from django.shortcuts import render

# Create your views here.
def show_main(request):
    # products = .objects.all()

    context = {
        'name': 'Pak Bepe', # Nama kamu
        'class': 'PBP A', # Kelas PBP kamu
        # 'products': products
    }

    return render(request, "preview.html", context)
