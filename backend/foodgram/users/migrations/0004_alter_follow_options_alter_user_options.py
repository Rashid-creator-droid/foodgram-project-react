# Generated by Django 4.2 on 2023-05-23 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_follow_уникальные_поля'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ['id'], 'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
