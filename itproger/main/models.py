from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator


class UserProfile(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Пользователь'),
        ('psychologist', 'Психолог'),
    ]

    GENDER_CHOICES = [
        ('m', 'Мужской'),
        ('f', 'Женский'),
    ]

    photo = models.ImageField(
        upload_to='psychologist_photos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )

    specializations = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Специализации"
    )

    about = models.TextField(
        max_length=600,
        blank=True,
        default='',
        verbose_name='О себе',
        help_text='Краткое описание вашего подхода к работе (до 500 символов)'
    )

    SPECIALIZATION_CHOICES = [
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

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    agreed_to_terms = models.BooleanField(default=False)  # Согласие с пользовательским соглашением
    role = models.CharField(max_length=12, choices=ROLE_CHOICES, default='user') #роль для пользователя и психолога

    # Новые поля для психолога
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(18), MaxValueValidator(100)])
    experience = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(80)]) #опыт работы
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    specializations = models.JSONField(blank=True, null=True)  # Будем хранить список специализаций
    photo = models.ImageField(upload_to='psychologist_photos/', blank=True, null=True)
    contacts = models.CharField(max_length=200, blank=True, null=True, verbose_name="Контакты")
    about = models.TextField(blank=True, null=True, max_length=300, verbose_name="О себе")

    def get_specializations_display(self):
        if not self.specializations:
            return []
        spec_names = {
            'stress': 'Стресс',
            'low_self-esteem': 'Низкая самооценка',
            'relationship_difficulties': 'Трудности в построении отношений',
            'relations_with_surroundings': 'Отношения с окружающими',
            'depressive_state': 'Депрессивное состояние',
            'panic_attacks_anxiety': 'Панические атаки, тревога',
            'social_adaptation_sociophobia': 'Социальная адаптация, социофобия',
            'adapting_to_new_conditions': 'Адаптация к новым условиям (переезд, поступление в ВУЗ)',
            'family_problems': 'Семейные проблемы',
            'parental_pressure': 'Давление со стороны родителей (учеба, выбор профессии)',
            'academic_performance_fear_of_exams': 'Проблемы с успеваемостью, страх экзаменов',
            'first_love_breakups': 'Первая любовь, расставания',
            'expressing_desires_assertiveness': 'Проявление желаний и отстаивание собственного мнения',
            'decision_making_goal_setting': 'Принятие решения, постановка цели',
            'burnout': 'Выгорание',
            'fears_phobias': 'Страхи и фобии',
            'loneliness': 'Одиночество',
            'neuroses_emotional_disorders': 'Неврозы и эмоциональные расстройства',
            'bullying': 'Буллинг',
            'aggressiveness_outbursts_of_anger': 'Агрессивность, приступы гнева',
            'sex_sexuality': 'Секс, сексуальность',
            'sleep_disorders_insomnia': 'Нарушения сна, бессонница',
            'bad_habits': 'Вредные привычки',
            'violence_trauma': 'Травма насилия',
            'obsessive_behavior_thoughts': 'Навязчивое поведение, мысли',
            'conflicts_with_teachers_professors': 'Конфликты с учителями/преподавателями',
            'death_of_a_close_person': 'Смерть близкого человека',
        }
        return [spec_names.get(spec, spec) for spec in self.specializations]

    def save(self, *args, **kwargs):
        # Убедимся, что специализации всегда сохраняются как список
        if not isinstance(self.specializations, list):
            self.specializations = []
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username