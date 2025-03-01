from .models import Articles #импортируем наш класс, который описывает работу с БД
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea #будем наследоваться от этого класса для работы с формами
from django import forms

class ArticlesForm(ModelForm):
    class Meta: #для определения метаданных формы создали вложенный класс
        model = Articles
        fields = ['title', 'anons', 'full_text', 'date'] #хотим отображать все данные, перечисляем их

        widgets = { #поле title создано на основе класса TextInput, прописываем атрибуты
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи'
            }),
            "anons": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Анонс статьи'
            }),
            "date": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата публикации'
            }),
            "full_text": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст статьи'
            }),
        }

class SearchForm(forms.Form): #создаем форму для поиска статьи
    query = forms.CharField(label='Поиск статьи', max_length=100) #Форма содержит одно текстовое поле с меткой "Поиск статьи", где пользователи могут вводить свой запрос. Максимальная длина текста, который можно ввести в поле, составляет 100 символов.