from django.urls import path
from . import views
from .views import custom_logout

urlpatterns = [
    path('', views.index, name='home'),  # Главная страница
    path('about/', views.about, name='about'),  # Страница "О нас"
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),  # Страница профиля
    path('accounts/logout/', custom_logout, name='logout'),
]