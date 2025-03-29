from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from .models import Articles, Like, Comment
from .forms import ArticlesForm, CommentForm
from django.views.generic import DetailView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from .decorators import psychologist_required
from django.core.exceptions import PermissionDenied
from django.db.models import F, Prefetch
from .forms import SearchForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

def news_home(request):
    search_query = request.GET.get('q', '')
    if search_query:
        news = Articles.objects.filter(title__icontains=search_query)
    else:
        news = Articles.objects.order_by('-date')
    return render(request, 'news/news_home.html', {'news': news, 'search_query': search_query})

class NewsDetailView(DetailView):
    model = Articles
    template_name = 'news/details_view.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()

        # Получаем все корневые комментарии с предзагрузкой ответов
        comments = self.object.comments.filter(parent__isnull=True) \
            .select_related('author') \
            .prefetch_related('likes', 'dislikes', 'replies__author', 'replies__likes', 'replies__dislikes')

        if self.request.user.is_authenticated:
            user = self.request.user
            liked_comments = Comment.objects.filter(
                likes=user, article=self.object
            ).values_list('id', flat=True)
            disliked_comments = Comment.objects.filter(
                dislikes=user, article=self.object
            ).values_list('id', flat=True)

            context['user_liked_comments'] = set(liked_comments)
            context['user_disliked_comments'] = set(disliked_comments)

        context['comments'] = comments
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Требуется авторизация'}, status=403)
            return redirect('login')

        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = request.user

            parent_id = request.POST.get('parent_id')
            if parent_id:
                try:
                    parent_comment = Comment.objects.get(id=parent_id, article=self.object)
                    comment.parent = parent_comment
                except Comment.DoesNotExist:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({'error': 'Родительский комментарий не найден'}, status=400)

            comment.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'comment_id': comment.id,
                    'parent_id': parent_id
                })

            return redirect('news-detail', pk=self.object.pk)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)

        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)

# Остальной код представлений остается без изменений

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


@csrf_exempt
@login_required
@require_POST
def like_article(request, pk):
    try:
        article = Articles.objects.get(pk=pk)
        like, created = Like.objects.get_or_create(
            user=request.user,
            article=article
        )

        if not created:
            like.delete()
            article.likes_count = max(0, article.likes_count - 1)
            liked = False
        else:
            article.likes_count += 1
            liked = True

        article.save()

        return JsonResponse({
            'liked': liked,
            'likes_count': article.likes_count
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@login_required
@require_POST
def like_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
        user = request.user

        if user in comment.likes.all():
            comment.likes.remove(user)
            liked = False
        else:
            # Удаляем из дизлайков если был
            if user in comment.dislikes.all():
                comment.dislikes.remove(user)
            comment.likes.add(user)
            liked = True

        return JsonResponse({
            'success': True,
            'liked': liked,
            'likes_count': comment.likes.count(),
            'disliked': False
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@login_required
@require_POST
def dislike_comment(request, pk):
    try:
        comment = Comment.objects.get(pk=pk)
        user = request.user

        if user in comment.dislikes.all():
            comment.dislikes.remove(user)
            disliked = False
        else:
            # Удаляем из лайков если был
            if user in comment.likes.all():
                comment.likes.remove(user)
            comment.dislikes.add(user)
            disliked = True

        return JsonResponse({
            'success': True,
            'disliked': disliked,
            'likes_count': comment.likes.count(),
            'liked': False
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)