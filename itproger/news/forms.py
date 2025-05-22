from django import forms
from django.core.validators import MaxLengthValidator
from .models import Articles, Comment, TAG_CHOICES

class ArticlesForm(forms.ModelForm):
    anons = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Анонс статьи (максимум 100 символов)',
            'maxlength': '100',
            'oninput': 'countChars(this, "anons-counter")'
        }),
        validators=[MaxLengthValidator(100)]
    )

    full_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Текст статьи (до 10,000 символов)',
            'rows': '15',
            'maxlength': '10000',
            'oninput': 'countChars(this, "text-counter")'
        }),
        validators=[MaxLengthValidator(10000)]
    )

    tags = forms.MultipleChoiceField(
        choices=TAG_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'tag-checkbox'
        }),
        required=False,
        label='Теги статьи'
    )

    class Meta:
        model = Articles
        fields = ['title', 'anons', 'full_text', 'photo', 'tags']
        widgets = {
            "title": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи'
            }),
            "photo": forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }
        labels = {
            'title': '',
            'anons': '',
            'full_text': '',
            'photo': 'Фотография для статьи',
        }
        help_texts = {
            'photo': 'Максимальный размер: 2MB',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.tags:
            self.initial['tags'] = self.instance.tags

    def save(self, commit=True):
        article = super().save(commit=False)
        article.tags = self.cleaned_data.get('tags', [])
        if commit:
            article.save()
            self.save_m2m()
        return article

class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск статьи', max_length=100)

class CommentForm(forms.ModelForm):
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Comment
        fields = ['text', 'parent_id']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Оставьте ваш комментарий...'
            })
        }
        labels = {
            'text': ''
        }
