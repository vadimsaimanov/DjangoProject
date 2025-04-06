from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .forms import PsychologistProfileForm
import logging

def index(request):
    data = {
        'title': 'Главная страница!',
        'values': ['Some', 'Hello', '123'],
        'obj': {
            'dar': 'BMW',
            'age': 18,
            'hobby': 'Football'
        }
    }
    return render(request, 'main/index.html', data)

def about(request):
    return render(request, 'main/about.html')

def test(request):
    return render(request, 'main/test.html')

def help(request):
    return render(request, 'main/help.html')

def searchpsy(request):
    return render(request, 'main/searchpsy.html')

# @login_required
# def profile_view(request):
#     return render(request, 'main/profile.html')

logger = logging.getLogger(__name__)


@login_required
def profile(request):
    # Очищаем старые сообщения при каждом запросе
    storage = messages.get_messages(request)
    for message in storage:
        pass  # Просто очищаем очередь сообщений

    if request.method == 'POST' and request.user.role == 'psychologist':
        post_data = request.POST.copy()
        if 'about' in post_data:
            post_data['about'] = post_data['about'][:500]

        form = PsychologistProfileForm(post_data, request.FILES, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False)
            user.contacts = form.cleaned_data['contacts']
            user.about = form.cleaned_data['about']

            if 'specializations' in form.cleaned_data:
                user.specializations = form.cleaned_data['specializations']

            user.save()

            # Очищаем сессию перед новым сообщением
            if 'profile_updated' in request.session:
                del request.session['profile_updated']

            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
        else:
            logger.error(f"Ошибки формы: {form.errors}")
            # Добавляем только одно сообщение об ошибке
            if not any(msg.message == 'Пожалуйста, исправьте ошибки в форме' for msg in messages.get_messages(request)):
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        if request.user.role == 'psychologist':
            form = PsychologistProfileForm(instance=request.user)
        else:
            form = None

    if 'logout' in request.POST:
        if 'profile_updated' in request.session:
            del request.session['profile_updated']
        messages.success(request, "Вы успешно вышли из системы.")
        return redirect('login')

    return render(request, 'main/profile.html', {
        'form': form,
        'user': request.user
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Проверяем, выбран ли чекбокс
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if remember_me:
                # Устанавливаем время жизни сессии на 2 недели
                request.session.set_expiry(1209600)  # 2 недели в секундах
            else:
                # Сессия закончится при закрытии браузера
                request.session.set_expiry(0)
            return redirect('profile')  # Перенаправляем на страницу профиля
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
            return render(request, 'main/login.html')
    return render(request, 'main/login.html')

def custom_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"Пользователь {user.username} успешно создан.")  # Отладочное сообщение
            login(request, user)
            return redirect('profile')
        else:
            print("Форма невалидна:", form.errors)  # Отладочное сообщение
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})