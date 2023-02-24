from rest_framework import serializers
from .models import SenderWallet, ReceiverWallet, CreateTransaction


class SenderWalletSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='creator.username')
    user_id = serializers.ReadOnlyField(source='creator.id')

    class Meta:
        model = SenderWallet
        fields = ['id', 'user', 'user_id', 'from_address', 'seed']


class ReceiverWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiverWallet
        fields = ['id', 'to_address', 'memo', 'tag']


class CreateTransactionSerializer(serializers.ModelSerializer):
    transaction_hash = serializers.ReadOnlyField()
    transaction_link = serializers.ReadOnlyField()

    class Meta:
        model = CreateTransaction
        fields = ['id', 'from_address', 'to_address', 'amount', 'transaction_hash', 'transaction_link']

