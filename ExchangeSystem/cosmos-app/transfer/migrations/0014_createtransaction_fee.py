# Generated by Django 4.1.6 on 2023-02-19 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0013_rename_pushedtransaction_publishtransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='createtransaction',
            name='fee',
            field=models.CharField(default='', max_length=50),
        ),
    ]
