from django.shortcuts import get_object_or_404
# from get_transaction_history import eth_get_transaction_history as eth_tx
from rest_framework import generics, permissions
import pickle
from .models import Wallet, Coin, Network, TransactionHistory
from .serializers import WalletSerializer, NetworkSerializer, CoinSerializer, TransactionHistorySerializer
from django.core.cache import cache
from .get_tx import btc_transaction_history, eth_get_transaction_history
from threading import Timer
from django.utils import timezone


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


class CoinsList(generics.ListCreateAPIView):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    permission_classes = [permissions.IsAuthenticated]


# class LatestTransactionsUpdater:
#     def __init__(self):
#         self.timer = None
#
#     def start(self):
#         print("updater started...")
#         self.update_transactions()
#
#     def update_transactions(self):
#         print("updating...")
#         # Get all wallets from the database
#         wallets = Wallet.objects.all()
#
#         # Loop through each wallet and retrieve the latest transactions
#         for wallet in wallets:
#             wallet_id = wallet.id
#             wallet_network = wallet.network
#             wallet_address = wallet.address
#             if wallet_network == 'btc':
#                 latest_txs = btc_transaction_history.get_transactions_btc(wallet_address)
#             else:
#                 latest_txs = {}
#
#             # Iterate through the transactions and update your database
#             for tx in latest_txs:
#                 print(tx)
#                 # Check if the transaction already exists in your database to avoid duplicates
#                 existing_tx = TransactionHistory.objects.filter(transaction_hash=tx).first()
#                 if not existing_tx:
#                     # Convert the transaction data to a dictionary compatible with the TransactionHistory model
#                     tx_data = {
#                         'transaction_hash': tx['id'],
#                         'amount': tx['amount'],
#                         'timestamp': timezone.make_aware(tx['timestamp']),
#                         'wallet_id': wallet_id,
#                     }
#
#                     # Create a new TransactionHistory object
#                     tx_obj = TransactionHistory(**tx_data)
#                     tx_obj.save()
#
#             # Invalidate the cached result for this wallet so that it will be refreshed on the next request
#             cache.delete(f'transactions_{wallet_id}')
#
#         # Schedule the next update in 5 minutes
#         # self.timer = Timer(1.0, self.update_transactions)
#         # self.timer.start()
#
#
# # updater = LatestTransactionsUpdater()
# # updater.start()


class TransactionHistoryList(generics.ListAPIView):
    serializer_class = TransactionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def update_transactions(self):
        print("updating...")
        # Get all wallets from the database
        wallets = Wallet.objects.all()

        # Loop through each wallet and retrieve the latest transactions
        for wallet in wallets:
            wallet_id = wallet.id
            wallet_network = str(wallet.network)
            wallet_address = str(wallet.address)
            print("wallet_network:", wallet_network)
            print("wallet_address:", wallet_address)
            if wallet_network == 'btc':
                print("wallet_network is btc")
                network = Network.objects.filter(name='btc').first()
                wallet = Wallet.objects.filter(address=wallet_address).first()
                coin = Coin.objects.filter(symbol='BTC', network=network).first()
                latest_txs = btc_transaction_history.get_transactions_btc(wallet_address)
                # print(latest_txs)
            if wallet_network == 'erc20':
                print("wallet_network is erc20")
                network = Network.objects.filter(name='erc20').first()
                wallet = Wallet.objects.filter(address=wallet_address).first()
                latest_txs = eth_get_transaction_history.get_erc20_history(wallet_address)
            else:
                latest_txs = {}

            # Iterate through the transactions and update your database
            for tx in latest_txs:
                # print("getting transactions...", tx)
                if wallet_network == 'erc20' and tx['contract_address'] != '':
                    coin = Coin.objects.filter(contract=tx['contract_address'], network=network).first()
                    if coin is None:
                        # print(network)
                        coin = Coin.objects.filter(symbol='no symbol', network=network).first()
                        # print(coin)

                elif wallet_network == 'erc20' and tx['contract_address'] == '':
                    coin = Coin.objects.filter(symbol='ETH', network=network).first()

                existing_tx = TransactionHistory.objects.filter(transaction_hash=tx['tx'], transaction_type=tx['type'], amount=tx['amount']).first()
                if not existing_tx:
                    # Convert the transaction data to a dictionary compatible with the TransactionHistory model
                    tx_data = {
                        'transaction_hash': tx['tx'],
                        'amount': tx['amount'],
                        'transaction_type': tx['type'],
                        'network': network,
                        'wallet': wallet,
                        'coin': coin
                    }
                    # Create a new TransactionHistory object
                    tx_obj = TransactionHistory(**tx_data)
                    tx_obj.save()

            # Invalidate the cached result for this wallet so that it will be refreshed on the next request
            cache.delete(f'transactions_{wallet_id}')

    def get_queryset(self):
        self.update_transactions()
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






