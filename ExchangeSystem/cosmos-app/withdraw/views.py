from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .models import AllCreateTransaction, AllSenderWallet, AllReceiverWallet
from .serializers import AllCreateTransactionSerializer, AllSenderWalletSerializer, AllReceiverWalletSerializer
from .broadcast_transaction import submit_transaction
import json
from django.core.cache import cache
import requests


class AllSenderWalletObject(generics.RetrieveDestroyAPIView):
    queryset = AllSenderWallet.objects.all()
    serializer_class = AllSenderWalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cache_key = f'all_sender_wallet_{self.kwargs["pk"]}'
        all_sender_wallet = cache.get(cache_key)

        if not all_sender_wallet:
            all_sender_wallet = get_object_or_404(AllSenderWallet, pk=self.kwargs['pk'])
            cache.set(cache_key, all_sender_wallet)

        return all_sender_wallet


class AllSenderWalletsList(generics.ListCreateAPIView):
    queryset = AllSenderWallet.objects.all()
    serializer_class = AllSenderWalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class AllReceiverWalletsList(generics.ListCreateAPIView):
    queryset = AllReceiverWallet.objects.all()
    serializer_class = AllReceiverWalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = AllReceiverWallet.objects.all()
        cache_key = 'all_receiver_wallets'

        receiver_wallets = cache.get(cache_key)
        if not receiver_wallets:
            receiver_wallets = list(queryset)
            cache.set(cache_key, receiver_wallets)

        return receiver_wallets


class AllReceiverWalletObject(generics.RetrieveDestroyAPIView):
    queryset = AllReceiverWallet.objects.all()
    serializer_class = AllReceiverWalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cache_key = f'all_receiver_wallet_{self.kwargs["pk"]}'
        receiver_wallet = cache.get(cache_key)

        if not receiver_wallet:
            receiver_wallet = get_object_or_404(AllReceiverWallet, pk=self.kwargs['pk'])
            cache.set(cache_key, receiver_wallet)

        return receiver_wallet


class AllCreateTransactionsList(generics.ListCreateAPIView):
    queryset = AllCreateTransaction.objects.all()
    serializer_class = AllCreateTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.validated_data['network'] == 'cardano':
            transaction_hash = self.cardano_get_transaction_hash(serializer.validated_data)
            serializer.save(transaction_hash=transaction_hash)
        elif serializer.validated_data['network'] == 'cosmos':
            transaction_hash = self.cosmos_get_transaction_hash(serializer.validated_data)
            serializer.save(transaction_hash=transaction_hash)

    def cardano_get_values(self, transaction):
        sender_wallet = transaction['from_address']
        receiver_wallet = transaction['to_address']

        return {'from_address': sender_wallet.from_address,
                "signing_key": sender_wallet.private_key, "to_address": receiver_wallet.to_address, "amount": transaction['amount']}

    def cardano_get_transaction_hash(self, transaction):
        response = self.cardano_get_values(transaction)
        print("Values Successfully Gathered.")
        return submit_transaction(response["from_address"], response["to_address"], response["amount"], json.dumps(response["signing_key"]))

    def cosmos_get_values(self, transaction):
        sender_wallet = transaction['from_address']
        receiver_wallet = transaction['to_address']
        seed = sender_wallet.private_key['seed']

        return {'from_address': sender_wallet.from_address,
                "seed": seed, "to_address": receiver_wallet.to_address, "amount": transaction['amount']}

    def cosmos_get_transaction_hash(self, transaction):
        response = self.cosmos_get_values(transaction)
        data = {"from_address": response["from_address"], "to_address": response["to_address"], "seed": response["seed"], "amount": response["amount"]}
        headers = {'Content-Type': 'application/json'}
        print("data", data)
        json_data = json.dumps(data)
        response = requests.post('http://ts:3000/api/broadcast-transaction/', data=json_data, headers=headers)
        if response.status_code == 201:
            data = response.json()
            return data['message']['transactionHash']
        else:
            print('API request failed with status code', response.status_code)


class AllCreateTransactionObject(generics.RetrieveDestroyAPIView):
    queryset = AllCreateTransaction.objects.all()
    serializer_class = AllCreateTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]