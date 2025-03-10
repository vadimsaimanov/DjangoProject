from django.contrib import admin #Эта строка импортирует модуль admin из пакета django.contrib. Модуль admin предоставляет функциональность для создания административной панели Django, которая позволяет управлять данными в вашем проекте.
from django.urls import path, include #Здесь импортируются функции path и include из модуля django.urls. path используется для создания URL-маршрутов. include позволяет включать другие файлы с URL-маршрутами (например, из других приложений), что помогает организовать код и делегировать обработку запросов.

from django.conf import settings #settings предоставляет доступ к настройкам вашего Django-проекта.
from django.conf.urls.static import static #static используется для обслуживания статических файлов (например, CSS, JavaScript, изображений) во время разработки.

urlpatterns = [
    path('admin/', admin.site.urls), #при переходе по ссылке admin, у нас будет открывать панель администратора
    path('', include('main.urls')), #пользователь переходит на главную страницу, мы передаем запрос в urls main
    path('news/', include('news.urls')), #если пользователь будет переходить по ссылки с именем news, то мы подключаем файл urls, который находится в приложении news
    path('ormsql/', include('ormsql.urls')),
    path('accounts/', include("django.contrib.auth.urls"))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)