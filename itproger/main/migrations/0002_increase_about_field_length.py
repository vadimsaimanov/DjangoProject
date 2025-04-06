from django.db import migrations, models

def set_empty_about(apps, schema_editor):
    UserProfile = apps.get_model('main', 'UserProfile')
    UserProfile.objects.filter(about__isnull=True).update(about='')

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),  # Убедитесь, что это последняя миграция вашего приложения
    ]

    operations = [
        migrations.RunPython(set_empty_about),
        migrations.AlterField(
            model_name='userprofile',
            name='about',
            field=models.TextField(
                max_length=500,
                blank=True,
                default='',
                verbose_name='О себе',
                help_text='Краткое описание вашего подхода к работе (до 500 символов)'
            ),
        ),
    ]
