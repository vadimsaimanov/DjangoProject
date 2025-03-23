from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE

User = get_user_model()  # Получаем модель пользователя

class Articles(models.Model): #создали класс, который наследуется от models, однако надо Наследование от models.Model: Вместо наследования от models, вы должны наследовать от models.Model. Это базовый класс для всех моделей в Django.
    id = models.AutoField(primary_key=True)
    title = models.CharField('Название', max_length=50, default='Новость') #создали поле название, первый параметр это подпись поля 'Название, в переменную вносим туда строку с ограничением по числу вводимых символов, если пользователь ничего не введет в поле, то будет задано значение по умолчанию
    anons = models.CharField('Анонс', max_length=250) #CharField тип имеет максимальную длину в 250 символов, подходит для короткой информации
    full_text = models.TextField('Статья') #в тип TextField можно вводить около 10-20 тысяч символов
    date = models.DateTimeField('Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')  # Добавляем поле автора
    views = models.PositiveIntegerField('Просмотры', default=0)  # Счетчик просмотров

    def __str__(self):
        return self.title #метод, определяет какая именно информация будет отображаться сама по себе

    def  get_absolute_url(self):
        return f'/news/{self.id}' #возвращение к той записи, которую обновляли

    class Meta: #переделываем название таблиц в панели админа
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'