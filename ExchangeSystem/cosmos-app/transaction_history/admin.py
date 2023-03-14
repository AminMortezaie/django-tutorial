from django.contrib import admin
from .models import Wallet, Network, Coin


admin.site.register(Wallet)
admin.site.register(Network)
admin.site.register(Coin)

