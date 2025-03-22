from django.http import HttpResponseForbidden
from functools import wraps

def psychologist_required(view_func):
    """
    Декоратор для проверки, что пользователь является психологом.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'psychologist':
            return HttpResponseForbidden("Доступ запрещен. Только для психологов.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view