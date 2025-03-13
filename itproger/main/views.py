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
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Перенаправляем на страницу профиля
        else:
            return render(request, 'main/login.html', {'error': 'Неверное имя пользователя или пароль'})
    return render(request, 'main/login.html')

def custom_logout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect('login')

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # Автоматически входим после регистрации
#             return redirect('profile')  # Перенаправляем на страницу профиля
#     else:
#         form = RegisterForm()
#     return render(request, 'main/register.html', {'form': form})

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