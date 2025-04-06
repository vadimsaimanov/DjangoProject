from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxLengthValidator

from .models import UserProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)
    agreed_to_terms = forms.BooleanField(required=True, label="Я согласен с пользовательским соглашением")
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, label="Роль")

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password1', 'password2', 'agreed_to_terms', 'role']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

class PsychologistProfileForm(forms.ModelForm):
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
        ('parental_pressure', 'Давление со стороны родителей (учёба, выбор профессии)'),
        ('academic_performance_fear_of_exams', 'Проблемы с успеваемостью, страх экзаменов'),
        ('first_love_breakups', 'Первая любовь, расставания'),
        ('expressing_desires_assertiveness', 'Проявление желаний и отстаивание собственного мнения'),
        ('decision_making_goal_setting', 'Принятие решений, постановка целей'),
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

    specializations = forms.MultipleChoiceField(
        choices=SPECIALIZATION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Специализации"
    )

    last_name = forms.CharField(label="Фамилия*", max_length=100)
    first_name = forms.CharField(label="Имя*", max_length=100)
    middle_name = forms.CharField(label="Отчество", max_length=100, required=False)
    age = forms.IntegerField(label="Возраст*")
    experience = forms.IntegerField(label="Опыт работы*")
    gender = forms.ChoiceField(label="Пол*", choices=UserProfile.GENDER_CHOICES)
    contacts = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Телефон/Email/Telegram'}),
        label="Контакты*",
        help_text="Укажите, как с вами можно связаться (телефон, email, мессенджеры)"
    )
    about = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'maxlength': '500',
            'data-max-length': '500',
        }),
        max_length=600,  # Серверное ограничение с запасом
        required=False,
        label="О себе*",
        help_text="Кратко опишите ваш подход к работе (до 500 символов)"
    )

    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'middle_name', 'age', 'experience',
            'gender', 'specializations', 'photo', 'about', 'contacts'
        ]
        widgets = {
            'about': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['age'].required = True
        self.fields['experience'].required = True
        self.fields['gender'].required = True
        self.fields['about'].required = True

        if self.instance and self.instance.specializations:
            self.initial['specializations'] = self.instance.specializations
