# Generated by Django 4.1.6 on 2023-02-15 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transfer', '0004_rename_user_senderwallet_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='senderwallet',
            name='creator',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]