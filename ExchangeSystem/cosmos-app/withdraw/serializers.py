from rest_framework import serializers
from .models import AllSenderWallet, AllReceiverWallet, AllCreateTransaction
from django.utils import timezone


class AllReceiverWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllReceiverWallet
        fields = '__all__'


class AllSenderWalletSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = AllSenderWallet
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {'id': data['id'], 'from_address': data['from_address'], 'network': data['network']}


class AllCreateTransactionSerializer(serializers.ModelSerializer):
    transaction_hash = serializers.ReadOnlyField()

    sender_address = serializers.CharField(max_length=100, default='from_address')
    receiver_address = serializers.CharField(max_length=100, default='to_address')
    amount = serializers.CharField(max_length=100, default='0')
    tx_hash = serializers.CharField(max_length=500, default="rejected", read_only=True)
    network = serializers.CharField(max_length=100, default='cardano')
    symbol = serializers.CharField(max_length=50, default='ada')
    midKey = serializers.CharField(max_length=100, default='')
    key = serializers.CharField(max_length=100, default='')
    timestamp = serializers.DateTimeField(default=timezone.now)

    class Meta:
        model = AllCreateTransaction
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {'id': data['id'], 'transaction_hash': data['transaction_hash']}

    def create(self, validated_data):
        # Remove fields from the validated data
        validated_data.pop('sender_address', None)
        validated_data.pop('receiver_address', None)
        validated_data.pop('amount', None)
        validated_data.pop('network', None)
        validated_data.pop('symbol', None)
        validated_data.pop('midKey', None)
        validated_data.pop('key', None)
        validated_data.pop('timestamp', None)

        # Create the object using the modified validated data
        instance = super().create(validated_data)
        return instance

    def validate_midKey(self, value):
        if value != 'midKey':
            raise serializers.ValidationError('MidKey is incorrect!')
        return value

    def validate_key(self, value):
        if value != 'key':
            raise serializers.ValidationError('Key is incorrect!')
        return value
