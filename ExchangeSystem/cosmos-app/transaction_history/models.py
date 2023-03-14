from django.db import models
from django.contrib.auth.admin import User
from datetime import datetime


class Network(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Wallet(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)


class Coin(models.Model):
    name = models.CharField(default='', max_length=100)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    contract = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TransactionHistory(models.Model):
    transaction_hash = models.CharField(max_length=100)
    amount = models.CharField(max_length=50)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    network = models.ForeignKey(Network, default='', on_delete=models.CASCADE)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'transaction_history_{wallet_id}'



