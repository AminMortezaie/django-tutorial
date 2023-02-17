from django.contrib import admin
from .models import SenderWallet, ReceiverWallet, CreateTransaction, PublishTransaction


admin.site.register(SenderWallet)
admin.site.register(ReceiverWallet)
admin.site.register(CreateTransaction)
admin.site.register(PublishTransaction)

