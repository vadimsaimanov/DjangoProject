# Generated by Django 5.1.6 on 2025-02-16 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ormsql', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table_1',
            fields=[
                ('id_name', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Table_2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='users',
            name='add_day',
            field=models.DateField(null=True),
        ),
    ]
