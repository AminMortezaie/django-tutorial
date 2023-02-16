from django.contrib import admin
from .models import SenderWallet, ReceiverWallet, CreateTransaction


admin.site.register(SenderWallet)
admin.site.register(ReceiverWallet)
admin.site.register(CreateTransaction)
