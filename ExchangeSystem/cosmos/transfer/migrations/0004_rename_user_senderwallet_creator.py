# Generated by Django 4.1.6 on 2023-02-15 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0003_senderwallet_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='senderwallet',
            old_name='user',
            new_name='creator',
        ),
    ]