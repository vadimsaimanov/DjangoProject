# Generated by Django 5.1.6 on 2025-03-14 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('user', 'Пользователь'), ('psychologist', 'Психолог')], default='user', max_length=12),
        ),
    ]
