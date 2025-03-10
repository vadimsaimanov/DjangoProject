from django.urls import path #подключаем дополнительно include, чтобы делегировать обязанностями по обработке запросов
from . import views

urlpatterns = [
    path('', views.index, name='home'), #имя прописываем, чтобы можно было менять название ссылки
    path('about/', views.about, name='about'),
    path('profile/', views.profile_view, name='profile')
]