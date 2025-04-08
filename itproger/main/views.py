from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404
from .forms import RegisterForm, PsychologistProfileForm
from .models import UserProfile
from django.contrib.postgres.search import TrigramSimilarity  # Для нечеткого поиска
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
import logging
from django.db.models import Count
from django.db.models import Q #Если в условии нужно использовать логическое ИЛИ, а также НЕ, то вместо перечисления критериев отбора через запятую, следует использовать специальный класс Q
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    if 'reset' in request.GET:
        return HttpResponseRedirect(reverse('searchpsy'))

    search_query = request.GET.get('q', '').strip()
    specializations = request.GET.getlist('specialization')
    sort_by = request.GET.get('sort', 'name_asc')
    gender = request.GET.get('gender', '')

    psychologists = UserProfile.objects.filter(role='psychologist')

    # Фильтрация по полу
    if gender:
        psychologists = psychologists.filter(gender=gender)

    # Нечеткий поиск
    if search_query:
        psychologists = psychologists.annotate(
            similarity=TrigramSimilarity('last_name', search_query) +
                       TrigramSimilarity('first_name', search_query) +
                       TrigramSimilarity('middle_name', search_query)
        ).filter(similarity__gt=0.3).order_by('-similarity')

    # Фильтрация по специализациям
    if specializations:
        query = Q()
        for spec in specializations:
            query |= Q(specializations__contains=[spec])
        psychologists = psychologists.filter(query)

    # Сортировка
    if sort_by == 'name_asc':
        psychologists = psychologists.order_by('last_name', 'first_name')
    elif sort_by == 'name_desc':
        psychologists = psychologists.order_by('-last_name', '-first_name')
    elif sort_by == 'exp_asc':
        psychologists = psychologists.order_by('experience')
    elif sort_by == 'exp_desc':
        psychologists = psychologists.order_by('-experience')

    paginator = Paginator(psychologists, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'selected_specializations': specializations,
        'sort_by': sort_by,
        'SPECIALIZATION_CHOICES': UserProfile.SPECIALIZATION_CHOICES
    }
    return render(request, 'main/searchpsy.html', context)


@login_required
def current_user_profile(request):
    """Профиль текущего пользователя (с возможностью редактирования)"""
    if request.method == 'POST':
        form = PsychologistProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            # Обработка специализаций
            specializations = request.POST.getlist('specializations')
            user.specializations = specializations
            user.save()
            messages.success(request, 'Профиль обновлен')
            return redirect('current_profile')
    else:
        form = PsychologistProfileForm(instance=request.user)

    return render(request, 'main/profile.html', {
        'form': form,
        'user': request.user,
        'editable': True
    })

logger = logging.getLogger(__name__)
def profile(request, user_id=None):
    from_search = request.GET.get('from_search', False)
    if user_id is None:
        if not request.user.is_authenticated:
            return redirect('login')
        user = request.user
        editable = True
    else:
        user = get_object_or_404(UserProfile, id=user_id)
        editable = request.user == user or request.user.is_superuser

    if request.method == 'POST' and editable and user.role == 'psychologist':
        form = PsychologistProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен')
            return redirect('profile', user_id=user.id)
    else:
        form = PsychologistProfileForm(instance=user) if editable and user.role == 'psychologist' else None

    return render(request, 'main/profile.html', {
        'user': user,
        'editable': editable,
        'form': form,
        'from_search': from_search
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
            return redirect('current_user_profile')  # Перенаправляем на страницу профиля
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
            return redirect('current_profile')
        else:
            print("Форма невалидна:", form.errors)  # Отладочное сообщение
    else:
        form = RegisterForm()
    return render(request, 'main/register.html', {'form': form})