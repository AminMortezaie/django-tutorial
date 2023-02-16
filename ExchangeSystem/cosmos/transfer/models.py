from django.db import models
from django.contrib.auth.admin import User


class SenderWallet(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    from_address = models.CharField(max_length=100)
    seed = models.CharField(max_length=300)
    private_key = models.BinaryField()
    account_number = models.IntegerField(default=0)
    sequence = models.IntegerField(default=0)
    memo = models.CharField(max_length=100, default='')


class ReceiverWallet(models.Model):
    to_address = models.CharField(max_length=100)
    tag = models.CharField(max_length=100, default='')


class CreateTransaction(models.Model):
    from_address = models.ForeignKey(SenderWallet, on_delete=models.CASCADE)
    to_address = models.ForeignKey(ReceiverWallet, on_delete=models.CASCADE)
    gas = models.CharField(max_length=50)
    amount = models.IntegerField(default=0)
    sync_mode = models.CharField(max_length=100, default="sync")
    chain_id = models.CharField(max_length=100, default="cosmoshub-4")


class PushableTransaction(models.Model):
    pass



