from django import forms
from django.contrib.auth.forms import UserCreationForm
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