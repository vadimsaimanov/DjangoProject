from django.shortcuts import render
from django.db.models import Q
from django.db.models import Count, Max, Min, Avg, Sum #для агрегирующих функций
import datetime
from .models import Users

def orm(request):
    # """простые запросы"""
    #SELECT * FROM ormsql_users
    # value = Users.objects.aggregate(Count('surname')) #агрегирующая функция count считает количество записей
    # value = Users.objects.aggregate(res=Sum('age') - Count('age'))#res для выражений
    value = ''
    # obj_list = Users.objects.order_by('id').all() #выводим все строки таблицы, если дописать values() то можно конкретные столбцы вывести. В коце можно сделать срез в квадратных скобках это же список
    # obj_list = Users.objects.filter(~Q(age__gte = 21) & Q(age__lte = 30)).all() #вместо where пищем слово filter для выборки данных
    # obj_list = Users.objects.filter(add_day__range=('2019-01-01', '2020-11-01')).all() #это как между BETWEEN
    # value = Users.objects.get(id=8) #получаем только одно поле
    # obj_list = Users.objects.filter(name__istartswith='а').all() #поиск по первой букве регистронезависимой
    # obj_list = Users.objects.filter(surname__isnull=False).all() #ищем ненулевые поля фамилии
    obj_list = Users.objects.values('class_type').annotate(Count('id')).order_by('class_type') #группируем и сортируем по полю class_type
    # obj_list = Users.objects.filter(age__in=[30, 35, 40]).all() #поиск или в скобках как OR
    # obj_list = []
    # element = Users(name='', surname='') #создали экземпляр класса с нужными нам параметрами, присваиваем его в переменную
    # element.save() #вызываем функциию save

    # Users.objects.create(name='', surname='')
    return render(request, 'ormsql/orm.html', {'obj_list': obj_list, 'value': value})

