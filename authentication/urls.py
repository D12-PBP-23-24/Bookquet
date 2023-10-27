from django.urls import path
from authentication.views import register #sesuaikan dengan nama fungsi yang dibuat
from authentication.views import login_user, logout_user #sesuaikan dengan nama fungsi yang dibuat

app_name = 'authentication'

urlpatterns = [
    path('register/', register, name='register'), #sesuaikan dengan nama fungsi yang dibuat
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]

