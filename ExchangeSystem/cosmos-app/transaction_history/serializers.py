from rest_framework import serializers
from .models import Wallet, Coin, Network, TransactionHistory
from django.utils import timezone


class WalletSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Wallet
        fields = '__all__'


class NetworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Network
        fields = '__all__'


class CoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coin
        fields= '__all__'


class TransactionHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionHistory
        fields = '__all__'

