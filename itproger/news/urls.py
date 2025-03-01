from django.urls import path #подключаем дополнительно include, чтобы делегировать обязанностями по обработке запросов
from . import views

urlpatterns = [
    path('', views.news_home, name='news_home'), #отслеживаем пустую строку, потому что пользователь к этому моменту уже находится в каталоге /news/
    path('create', views.create, name='create'),
    path('<int:pk>', views.NewsDetailView.as_view(), name='news-detail'), #динамически отслеживаем целочисленное число, назовем его pk первичный ключ, пробелы не ставить между двоиточием инт и pk. В этот раз мы не метод вызываем, а класс. Обязательно дописываем метод as_view(), иначе ошибка.
    path('<int:pk>/update', views.NewsUpdateView.as_view(), name='news-update'),
    path('<int:pk>/delete', views.NewsDeleteView.as_view(), name='news-delete'),
]