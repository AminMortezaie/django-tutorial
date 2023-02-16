from django.contrib import admin
from .models import SenderWallet
from .models import ReceiverWallet
from .models import CreateTransaction


admin.site.register(SenderWallet)
admin.site.register(ReceiverWallet)
admin.site.register(CreateTransaction)
