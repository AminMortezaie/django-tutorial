# Generated by Django 4.1.6 on 2023-02-22 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0015_remove_createtransaction_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publishtransaction',
            name='response',
        ),
        migrations.AddField(
            model_name='publishtransaction',
            name='transaction_hash',
            field=models.CharField(default='rejected', max_length=500),
        ),
    ]