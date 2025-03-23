from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect #Функция render используется для отображения HTML-шаблона и передачи контекста в него.
from .models import Articles #импортируем модель, класс который нам нужен для работы с таблицей
from .forms import ArticlesForm
from django.views.generic import DetailView, UpdateView, DeleteView #на основе этого класса можно создать страницу, которая будет постоянно изменятья в зависимости от параметра в url адрессе
from django.utils.decorators import method_decorator #позволяет применять декораторы к методам классов
from .decorators import psychologist_required
from django.core.exceptions import PermissionDenied
from django.db.models import F
from .forms import SearchForm

# def news_home(request):
#     news = Articles.objects.order_by('-date')#[:4] в квадратных скобках можно указать срез, сколько отображать записей на странице #добавили все содержимое таблицы в переменную
#     return render(request, 'news/news_home.html', {'news': news}) #возвращаем html шаблон, все шаблоны лежат в одном месте
def news_home(request):
    search_query = request.GET.get('q', '')  # Получаем поисковый запрос из URL

    if search_query:
        # Фильтруем статьи по названию (регистронезависимый поиск)
        news = Articles.objects.filter(title__icontains=search_query)
    else:
        # Если запроса нет, показываем все статьи, отсортированные по дате
        news = Articles.objects.order_by('-date')

    return render(request, 'news/news_home.html', {'news': news, 'search_query': search_query})

class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        # Получаем статью
        self.object = self.get_object()

        # Увеличиваем счетчик просмотров, если пользователь не автор статьи
        if request.user != self.object.author:
            Articles.objects.filter(pk=self.object.pk).update(views=F('views') + 1)

        # Передаем контекст в шаблон
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class AuthorOrAdminRequiredMixin:
    """
    Миксин для проверки, что пользователь является автором статьи или администратором.
    """
    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()  # Получаем статью
        if not (request.user == article.author or request.user.is_superuser):
            raise PermissionDenied("У вас нет прав для выполнения этого действия.")
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
@method_decorator(psychologist_required, name='dispatch')
class NewsUpdateView(AuthorOrAdminRequiredMixin, UpdateView):
    model = Articles
    template_name = 'news/news-update.html'
    form_class = ArticlesForm

@method_decorator(login_required, name='dispatch')
@method_decorator(psychologist_required, name='dispatch')
class NewsDeleteView(AuthorOrAdminRequiredMixin, DeleteView):
    model = Articles
    success_url = '/news'
    template_name = 'news/news-delete.html'

@login_required
@psychologist_required
def create(request):
    error = ''
    if request.method == 'POST': #метод передачи данных post, исполняется когда жмем на кнопку добавить
        form = ArticlesForm(request.POST) #здесь хранятся все дданные получченные из формы которую заполнил пользователь
        if form.is_valid(): #проверяем, являются ли данные корректно заполненными, тогда сохраняем
            article = form.save(commit=False)  # Создаем объект статьи, но не сохраняем в базу
            article.author = request.user  # Устанавливаем автора статьи
            article.save()  # Теперь сохраняем статью в базу
            return redirect('/news') #возврат на страницу со всеми новостями
        else:
            error = 'Форма неверно заполнена'

    else:
        form = ArticlesForm()#создали объект класса

    data = {
        'form': form,
        'eror': error
    }

    return render(request, 'news/create.html', data)


