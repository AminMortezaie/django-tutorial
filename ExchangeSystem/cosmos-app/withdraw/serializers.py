from rest_framework import serializers
from .models import AllSenderWallet, AllReceiverWallet, AllCreateTransaction


class AllCreateTransactionSerializer(serializers.ModelSerializer):
    transaction_hash = serializers.ReadOnlyField()

    class Meta:
        model = AllCreateTransaction
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {'id': data['id'], 'transaction_hash': data['transaction_hash']}

    def create(self, validated_data):
        network = validated_data.pop('network')
        instance = super().create(validated_data)
        instance.network = network
        instance.save()
        return instance


class AllReceiverWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllReceiverWallet
        fields = '__all__'


class AllSenderWalletSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = AllSenderWallet
        fields = '__all__'
