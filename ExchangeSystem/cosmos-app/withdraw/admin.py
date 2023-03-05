from django.contrib import admin

# Register your models here.
from .models import AllCreateTransaction, AllSenderWallet, AllReceiverWallet


admin.site.register(AllSenderWallet)
admin.site.register(AllReceiverWallet)
admin.site.register(AllCreateTransaction)
