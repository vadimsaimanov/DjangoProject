from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm

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

@login_required
def profile_view(request):
    return render(request, 'main/profile.html')

@login_required
def profile(request):
    return render(request, 'main/profile.html')

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