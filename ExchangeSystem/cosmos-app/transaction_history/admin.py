from django.contrib import admin
from .models import Wallet, Network, Coin, TransactionHistory


admin.site.register(Wallet)
admin.site.register(Network)
admin.site.register(Coin)
admin.site.register(TransactionHistory)
