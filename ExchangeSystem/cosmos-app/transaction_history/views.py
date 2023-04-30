from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions
import pickle
from .models import Wallet, Coin, Network, TransactionHistory
from .serializers import WalletSerializer, NetworkSerializer, CoinSerializer, TransactionHistorySerializer
from django.core.cache import cache
from .get_tx import btc_transaction_history, eth_get_transaction_history
from .tasks import update_transactions, update_transactions_bep20, update_transactions_getblock


class WalletObject(generics.RetrieveDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cache_key = f'wallet_{self.kwargs["pk"]}'
        wallet = cache.get(cache_key)

        if not wallet:
            wallet = get_object_or_404(Wallet, pk=self.kwargs['pk'])
            cache.set(cache_key, wallet)

        return wallet


class WalletsList(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]


class NetworkObject(generics.RetrieveDestroyAPIView):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cache_key = f'network_{self.kwargs["pk"]}'
        network = cache.get(cache_key)

        if not network:
            network = get_object_or_404(Network, pk=self.kwargs['pk'])
            cache.set(cache_key, network)

        return network


class NetworksList(generics.ListCreateAPIView):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    permission_classes = [permissions.IsAuthenticated]


class CoinObject(generics.RetrieveDestroyAPIView):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cache_key = f'coin_{self.kwargs["pk"]}'
        coin = cache.get(cache_key)

        if not coin:
            coin = get_object_or_404(Coin, pk=self.kwargs['pk'])
            cache.set(cache_key, coin)

        return coin


def check_for_duplication(data):
    if (data['network'] == Network.objects.filter(name='erc20').first()) or \
            (data['network'] == Network.objects.filter(name='bsc').first()):
        existing_coin = Coin.objects.filter(contract=str(data['contract']).lower(), network=data['network'], symbol=data['symbol'])
    else:
        existing_coin = Coin.objects.filter(contract=data['contract'], network=data['network'], symbol=data['symbol'])

    if existing_coin:
        raise ValidationError("Duplication Error. Coin is available..")


class CoinsList(generics.ListCreateAPIView):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        data = dict(serializer.validated_data)
        check_for_duplication(data)
        if (data['network'] == Network.objects.filter(name='erc20').first()) or (data['network'] == Network.objects.filter(name='bsc').first()):
            print("network is erc20 or bsc in saving coins.")
            serializer.save(contract=str(data['contract']).lower())
        else:
            serializer.save()


class TransactionHistoryList(generics.ListAPIView):
    serializer_class = TransactionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        wallet_id = self.kwargs['wallet_id']
        cached_result = cache.get(f'transactions_{wallet_id}')

        if cached_result:
            # Deserialize the cached result and return it
            return pickle.loads(cached_result)

        # If the result is not cached, retrieve it from the database and cache it
        queryset = TransactionHistory.objects.filter(wallet_id=wallet_id).order_by('-timestamp')[:200]
        cache.set(f'transactions_{wallet_id}', pickle.dumps(queryset))
        cache.expire(f'transactions_{wallet_id}', 300)  # Set expiration time to 5 minutes

        return queryset




