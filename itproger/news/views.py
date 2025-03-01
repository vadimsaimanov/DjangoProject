from django.shortcuts import render, redirect #Функция render используется для отображения HTML-шаблона и передачи контекста в него.
from .models import Articles #импортируем модель, класс который нам нужен для работы с таблицей
from .forms import ArticlesForm
from django.views.generic import DetailView, UpdateView, DeleteView #на основе этого класса можно создать страницу, которая будет постоянно изменятья в зависимости от параметра в url адрессе
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

class NewsDetailView(DetailView): #полностью наследуемся от класса DetailView
    model = Articles  # работаем с моделью (базой данных) Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article' #как ключ, по которому будем передавать запись из бд внутрь шаблона

class NewsUpdateView(UpdateView):
    model = Articles  # работаем с моделью (базой данных) Articles
    template_name = 'news/news-update.html'

    form_class = ArticlesForm #атрибут, который используется в классах представлений Django, таких как UpdateView, для указания, какую форму использовать при обработке данных.

class NewsDeleteView(DeleteView):
    model = Articles  # работаем с моделью (базой данных) Articles
    success_url = '/news'
    template_name = 'news/news-delete.html'

def create(request):
    error = ''
    if request.method == 'POST': #метод передачи данных post, исполняется когда жмем на кнопку добавить
        form = ArticlesForm(request.POST) #здесь хранятся все дданные получченные из формы которую заполнил пользователь
        if form.is_valid(): #проверяем, являются ли данные корректно заполненными, тогда сохраняем
            form.save()
            return redirect('/news') #возврат на страницу со всеми новостями
        else:
            error = 'Форма неверно заполнена'

    form = ArticlesForm()#создали объект класса

    data = {
        'form': form,
        'eror': error
    }

    return render(request, 'news/create.html', data)


