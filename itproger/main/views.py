from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect #импортиреум redirect: Эта функция создаёт HTTP-ответ с перенаправлением. Она применяется для отправки браузера пользователя на другой URL-адрес. render:  Эта функция используется для отрисовки шаблона (HTML-файла) с контекстными данными (переменными, которые будут использоваться внутри шаблона) и возврата HTTP-ответа.  Это стандартный способ отображения динамического контента в веб-приложениях на Django.
# from django.http import HttpResponse #это класс в Django, который используется для создания HTTP-ответов, которые отправляются клиенту (обычно веб-браузеру) в ответ на HTTP-запросы.
from django.contrib.auth import authenticate, login, logout #подключаем библиотеки для логина авторизации и разлогинивания

def index(request): #обязательно должен быть параметр, получаем запрос request
    # print(request.user)
    data = { #словарь, что хотим передать в html
        'title': 'Главная страница!',
        'values': ['Some', 'Hello', '123'],
        'obj': {
            'dar': 'BMW',
            'age': 18,
            'hobby': 'Football'
        }

    }
    return render(request, 'main/index.html', data) #вызываем нужный html шаблон

def about(request): #обязательно должен быть параметр, получаем запрос request
    return render(request, 'main/about.html')

# def notice(request): #обязательно должен быть параметр, получаем запрос request
#     return HttpResponse("<h4>Если вы чувствуюете, что больше не можете, обратитесь по номеру ###</h4>") #возвращаем на страничку сайта ответ на запрос

@login_required
def profile_view(request):
    return render(request, 'main/profile.html')