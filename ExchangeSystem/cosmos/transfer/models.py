from django.db import models
from django.contrib.auth.admin import User


class SenderWallet(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    from_address = models.CharField(max_length=100)
    seed = models.CharField(max_length=300)


class ReceiverWallet(models.Model):
    to_address = models.CharField(max_length=100)
    tag = models.CharField(max_length=100, default='')
    memo = models.CharField(max_length=100, default='')


class CreateTransaction(models.Model):
    from_address = models.ForeignKey(SenderWallet, on_delete=models.CASCADE)
    to_address = models.ForeignKey(ReceiverWallet, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100, default='0')
    transaction_hash = models.CharField(max_length=500, default="rejected")
    transaction_link = models.CharField(max_length=1000, default='')




