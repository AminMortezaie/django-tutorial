from rest_framework import serializers
from .models import SenderWallet
from .models import ReceiverWallet
from .models import CreateTransaction


class SenderWalletSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='creator.username')
    user_id = serializers.ReadOnlyField(source='creator.id')
    private_key = serializers.ReadOnlyField()

    class Meta:
        model = SenderWallet
        fields = ['id', 'user', 'user_id', 'from_address', 'seed', 'private_key', 'account_number', 'sequence', 'memo']


class ReceiverWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiverWallet
        fields = ['id', 'to_address']


class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreateTransaction
        fields = ['id', 'from_address', 'to_address', 'gas', 'amount', 'sync_mode', 'chain_id']
