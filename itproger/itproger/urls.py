from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # Подключаем маршруты приложения main
    path('news/', include('news.urls')),  # Подключаем маршруты приложения news
    path('ormsql/', include('ormsql.urls')),  # Подключаем маршруты приложения ormsql
    path('accounts/', include('django.contrib.auth.urls')),  # Встроенные маршруты для аутентификации
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),  # Кастомный маршрут для логина
    path('accounts/logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Кастомный маршрут для логаута
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)