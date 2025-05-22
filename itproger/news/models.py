from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError  # Импортируем ValidationError
from django.utils import timezone

User = get_user_model()

TAG_CHOICES = [
    ('stress', 'Стресс'),
    ('low_self-esteem', 'Низкая самооценка'),
    ('relationship_difficulties', 'Трудности в построении отношений'),
    ('relations_with_surroundings', 'Отношения с окружающими'),
    ('depressive_state', 'Депрессивное состояние'),
    ('panic_attacks_anxiety', 'Панические атаки, тревога'),
    ('social_adaptation_sociophobia', 'Социальная адаптация, социофобия'),
    ('adapting_to_new_conditions', 'Адаптация к новым условиям (переезд, поступление в ВУЗ)'),
    ('family_problems', 'Семейные проблемы'),
    ('parental_pressure', 'Давление со стороны родителей (учеба, выбор профессии)'),
    ('academic_performance_fear_of_exams', 'Проблемы с успеваемостью, страх экзаменов'),
    ('first_love_breakups', 'Первая любовь, расставания'),
    ('expressing_desires_assertiveness', 'Проявление желаний и отстаивание собственного мнения'),
    ('decision_making_goal_setting', 'Принятие решения, постановка цели'),
    ('burnout', 'Выгорание'),
    ('fears_phobias', 'Страхи и фобии'),
    ('loneliness', 'Одиночество'),
    ('neuroses_emotional_disorders', 'Неврозы и эмоциональные расстройства'),
    ('bullying', 'Буллинг'),
    ('aggressiveness_outbursts_of_anger', 'Агрессивность, приступы гнева'),
    ('sex_sexuality', 'Секс, сексуальность'),
    ('sleep_disorders_insomnia', 'Нарушения сна, бессонница'),
    ('bad_habits', 'Вредные привычки'),
    ('violence_trauma', 'Травма насилия'),
    ('obsessive_behavior_thoughts', 'Навязчивое поведение, мысли'),
    ('conflicts_with_teachers_professors', 'Конфликты с учителями/преподавателями'),
    ('death_of_a_close_person', 'Смерть близкого человека'),
]

class Articles(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField('Название', max_length=50)
    anons = models.CharField('Анонс', max_length=250)
    full_text = models.TextField('Статья')
    date = models.DateTimeField('Дата публикации', default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    views = models.PositiveIntegerField('Просмотры', default=0)
    likes_count = models.PositiveIntegerField(default=0)
    photo = models.ImageField(
        'Фотография',
        upload_to='news_photos/',
        null=True,
        blank=True,
        help_text='Загрузите фотографию для статьи'
    )
    tags = models.JSONField(
        'Теги',
        default=list,
        blank=True,
        help_text='Выберите теги статьи'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def clean(self):
        # Валидация длины аннотации
        if len(self.anons) > 100:
            raise ValidationError({'anons': 'Анонс не должен превышать 100 символов'})

        # Валидация размера фотографии
        if self.photo:
            if self.photo.size > 2 * 1024 * 1024:  # 2MB
                raise ValidationError({'photo': 'Фотография не должна превышать 2MB'})

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