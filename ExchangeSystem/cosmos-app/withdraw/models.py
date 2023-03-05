from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.admin import User


def get_empty_dict():
    return {}


class AllSenderWallet(models.Model):
    creator = models.ForeignKey(User, default='', on_delete=models.CASCADE)
    from_address = models.CharField(max_length=100)
    network = models.CharField(max_length=100, default='cardano')
    private_key = models.JSONField(default='')


class AllReceiverWallet(models.Model):
    to_address = models.CharField(max_length=100)
    tag = models.CharField(max_length=100, default='')
    memo = models.CharField(max_length=100, default='')
    network = models.CharField(max_length=100, default='cardano')


class AllCreateTransaction(models.Model):
    from_address = models.ForeignKey(AllSenderWallet, on_delete=models.CASCADE)
    to_address = models.ForeignKey(AllReceiverWallet, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, default='0')
    transaction_hash = models.CharField(max_length=500, default="rejected")
    network = models.CharField(max_length=100, default='cardano')
    symbol = models.CharField(max_length=50, default='ada')
    midKey = models.CharField(max_length=100, default='')
    key = models.CharField(max_length=100, default='')
    timestamp = models.DateTimeField(auto_now_add=True)




