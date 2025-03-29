from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError  # Импортируем ValidationError
from django.utils import timezone

User = get_user_model()

class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField('Название', max_length=50, default='Новость')
    anons = models.CharField('Анонс', max_length=250)
    full_text = models.TextField('Статья')
    date = models.DateTimeField('Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    views = models.PositiveIntegerField('Просмотры', default=0)
    likes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')


class Comment(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField('Текст комментария')
    created_date = models.DateTimeField('Дата создания', default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)

    class Meta:
        ordering = ['created_date']

    def get_reply_count(self):
        return self.replies.count()

    def get_all_replies(self):
        return self.replies.all().select_related('author').prefetch_related('likes', 'dislikes')