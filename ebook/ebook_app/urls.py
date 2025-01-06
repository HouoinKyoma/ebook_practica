from django.urls import path 
from ebook_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', lambda request: redirect('home'), name='profile_redirect'),
    path('add_to_favorites/<int:ebook_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.favorite_books, name='favorites'),
    path('remove_from_favorites/<int:ebook_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('book_detail/<int:id>/', views.book_detail, name='book_detail'),
    path('search/', views.ebook_search, name='search_ebooks'),
] + static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

