from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.admin import User
from datetime import datetime

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
    transaction_hash = models.CharField(max_length=500, default="rejected")




