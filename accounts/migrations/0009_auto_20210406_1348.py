# Generated by Django 3.1.7 on 2021-04-06 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210405_0359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorite',
            name='favorite',
        ),
        migrations.AddField(
            model_name='favorite',
            name='favorite',
            field=models.ManyToManyField(related_name='user_favoured', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_favorites', to=settings.AUTH_USER_MODEL),
        ),
    ]