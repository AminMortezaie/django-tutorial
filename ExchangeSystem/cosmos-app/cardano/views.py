from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .models import CardanoSenderWallet, CardanoReceiverWallet, CardanoCreateTransaction
from .serializers import CardanoSenderWalletSerializer, CardanoReceiverWalletSerializer, CardanoCreateTransactionSerializer
import requests
import json
from django.core.cache import cache


class CardanoSenderWalletObject(generics.RetrieveDestroyAPIView):
    queryset = CardanoSenderWallet.objects.all()
    serializer_class = CardanoSenderWalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cache_key = f'cardano_sender_wallet_{self.kwargs["pk"]}'
        sender_wallet = cache.get(cache_key)

        if not sender_wallet:
            sender_wallet = get_object_or_404(CardanoSenderWallet, pk=self.kwargs['pk'])
            cache.set(cache_key, sender_wallet)

        return sender_wallet


class CardanoSenderWalletList(generics.ListCreateAPIView):
    queryset = CardanoSenderWallet.objects.all()
    serializer_class = CardanoSenderWalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CardanoReceiverWalletList(generics.ListCreateAPIView):
    queryset = CardanoReceiverWallet.objects.all()
    serializer_class = CardanoReceiverWalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = CardanoReceiverWallet.objects.all()
        cache_key = 'cardano_receiver_wallets'

        receiver_wallets = cache.get(cache_key)
        if not receiver_wallets:
            receiver_wallets = list(queryset)
            cache.set(cache_key, receiver_wallets)

        return receiver_wallets


class CardanoReceiverWalletObject(generics.RetrieveDestroyAPIView):
    queryset = CardanoReceiverWallet.objects.all()
    serializer_class = CardanoReceiverWalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cache_key = f'cardano_receiver_wallet_{self.kwargs["pk"]}'
        receiver_wallet = cache.get(cache_key)

        if not receiver_wallet:
            receiver_wallet = get_object_or_404(CardanoReceiverWallet, pk=self.kwargs['pk'])
            cache.set(cache_key, receiver_wallet)

        return receiver_wallet


class CardanoCreateTransactionsList(generics.ListCreateAPIView):
    queryset = CardanoCreateTransaction.objects.all()
    serializer_class = CardanoCreateTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # transaction_hash = self.get_response_from_transfer_request(serializer.validated_data)
        # serializer.save(transaction_hash=transaction_hash, transaction_link="https://preview.cexplorer.io/tx/"+transaction_hash)
        print(self.get_values(serializer.validated_data))
        serializer.save(transaction_hash='', transaction_link='')

    def get_values(self, transaction):
        sender_wallet = transaction['from_address']
        receiver_wallet = transaction['to_address']

        return {'from_address': sender_wallet.from_address,
                "singing_key": sender_wallet.signing_key, "to_address": receiver_wallet.to_address, "amount": transaction['amount']}


class CardanoCreateTransactionObject(generics.RetrieveDestroyAPIView):
    queryset = CardanoCreateTransaction.objects.all()
    serializer_class = CardanoCreateTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


