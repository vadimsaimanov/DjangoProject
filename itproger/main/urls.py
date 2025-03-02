from django.urls import path #подключаем дополнительно include, чтобы делегировать обязанностями по обработке запросов
from . import views

urlpatterns = [
    path('', views.index, name='home'), #имя прописываем, чтобы можно было менять название ссылки
    path('about', views.about, name='about'),
    # path('login/', views.user_login, name='login'), #логин пользователя
    # path('logout/', views.user_logout, name='logout'), #выход из аккаунта
    path('profile', views.profile_view, name='profile')
]