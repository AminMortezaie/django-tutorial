# Generated by Django 4.1.7 on 2023-02-25 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0020_receiverwallet_creator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receiverwallet',
            name='creator',
        ),
    ]
