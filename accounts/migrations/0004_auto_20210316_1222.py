# Generated by Django 3.1.7 on 2021-03-16 11:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'ordering': ('created_at',)},
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_online',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
