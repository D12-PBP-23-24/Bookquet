"""
URL configuration for Bookquet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from book_preview.views import show_preview, add_rating_comment, recomendation_book, update_global_filter_settings, filter_comments

app_name = 'book_preview'

urlpatterns = [
    path('preview/<int:book_id>/', show_preview, name='show_preview'),
    path('review/<int:book_id>/', add_rating_comment, name='add_rating_comment'),
    path('preview/json/<int:book_id>', recomendation_book, name="book_recomendation_json"),
    path('filter-comments/<str:filter_type>/', filter_comments, name='filter_comments'),
    path('update-global-filter/', update_global_filter_settings, name='update_global_filter_settings'),
]
