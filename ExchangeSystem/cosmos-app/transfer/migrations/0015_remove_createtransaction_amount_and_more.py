# Generated by Django 4.1.6 on 2023-02-22 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transfer', '0014_createtransaction_fee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createtransaction',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='createtransaction',
            name='chain_id',
        ),
        migrations.RemoveField(
            model_name='createtransaction',
            name='fee',
        ),
        migrations.RemoveField(
            model_name='createtransaction',
            name='gas',
        ),
        migrations.RemoveField(
            model_name='createtransaction',
            name='sync_mode',
        ),
        migrations.RemoveField(
            model_name='senderwallet',
            name='account_number',
        ),
        migrations.RemoveField(
            model_name='senderwallet',
            name='private_key',
        ),
        migrations.RemoveField(
            model_name='senderwallet',
            name='sequence',
        ),
    ]