from django.db import models
from django.db.models.deletion import CASCADE

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=True)
    # surname = models.CharField(max_length=128, null=True)
    # add_day = models.DateField(null=True)
    # age = models.IntegerField(null=True)
    # active = models.BooleanField(null=True)
    # class_type = models.IntegerField(null=True)
#перевели строки таблицы в читаемый строковый тип
    def __str__(self):
        return f'{self.name} | {self.surname} | {self.add_day} | {self.age} | {self.active} | {self.class_type}'

class Lessons(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', on_delete=CASCADE)
    event_day = models.DateField(null=True)
    lesson_time = models.IntegerField(null=True)

class Steps(models.Model):
    lesson_m2m = models.ManyToManyField(Lessons)
    id = models.AutoField(primary_key=True)
    step_name = models.CharField(max_length=128, null=True)

class Categories(models.Model):
    m2m = models.ManyToManyField(Users) #укахываем связь мэни ту мэни многие ко многим с таблицей Users создает третью таблицу
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class Table_1(models.Model):
    id_name = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=True)

class Table_2(models.Model):
    name = models.CharField(max_length=128, null=True)

class Table_3(models.Model):
    id_name = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=True)

class Table_4(models.Model):
    name = models.CharField(max_length=128, null=True)
    fk_field = models.ForeignKey(Table_3, on_delete=CASCADE) #внешний ключ - ссылаемся на 3 таблицу, каскад говорит, если удалить таблицу, на которую ссылаемся, то и эта тоже удалится
