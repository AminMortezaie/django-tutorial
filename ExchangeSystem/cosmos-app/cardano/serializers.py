from rest_framework import serializers
from .models import CardanoSenderWallet, CardanoReceiverWallet, CardanoCreateTransaction


class CardanoSenderWalletSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='creator.username')
    user_id = serializers.ReadOnlyField(source='creator.id')

    class Meta:
        model = CardanoSenderWallet
        fields = ['id', 'user', 'user_id', 'from_address', 'signing_key']


class CardanoReceiverWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardanoReceiverWallet
        fields = ['id', 'to_address', 'tag']


class CardanoCreateTransactionSerializer(serializers.ModelSerializer):
    transaction_hash = serializers.ReadOnlyField()
    transaction_link = serializers.ReadOnlyField()

    class Meta:
        model = CardanoCreateTransaction
        fields = ['id', 'from_address', 'to_address', 'amount', 'transaction_hash', 'transaction_link']

