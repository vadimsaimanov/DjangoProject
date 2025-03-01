from django.urls import path #подключаем дополнительно include, чтобы делегировать обязанностями по обработке запросов
from . import views

urlpatterns = [
    path('', views.orm, name='orm') #имя прописываем, чтобы можно было менять название ссылки
]