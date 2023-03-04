from django.contrib import admin
from .models import CardanoSenderWallet, CardanoReceiverWallet, CardanoCreateTransaction


admin.site.register(CardanoSenderWallet)
admin.site.register(CardanoReceiverWallet)
admin.site.register(CardanoCreateTransaction)
