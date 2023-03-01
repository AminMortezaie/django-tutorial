from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .models import CardanoSenderWallet, CardanoReceiverWallet, CardanoCreateTransaction
from .serializers import CardanoSenderWalletCreateSerializer, CardanoSenderWalletRetrieveSerializer, CardanoReceiverWalletSerializer, CardanoCreateTransactionSerializer
from .broadcast_transaction import submit_transaction
import json
from django.core.cache import cache


class CardanoSenderWalletObject(generics.RetrieveDestroyAPIView):
    queryset = CardanoSenderWallet.objects.all()
    serializer_class = CardanoSenderWalletRetrieveSerializer
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
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CardanoSenderWalletCreateSerializer
        else:
            return CardanoSenderWalletRetrieveSerializer

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
        transaction_hash = self.get_transaction_hash(serializer.validated_data)
        serializer.save(transaction_hash=transaction_hash, transaction_link="https://preview.cexplorer.io/tx/"+transaction_hash)

    def get_values(self, transaction):
        sender_wallet = transaction['from_address']
        receiver_wallet = transaction['to_address']

        return {'from_address': sender_wallet.from_address,
                "signing_key": sender_wallet.signing_key, "to_address": receiver_wallet.to_address, "amount": transaction['amount']}

    def get_transaction_hash(self, transaction):
        response = self.get_values(transaction)
        print("Values Successfully Gathered.")
        return submit_transaction(response["from_address"], response["to_address"], response["amount"], json.dumps(response["signing_key"]))


class CardanoCreateTransactionObject(generics.RetrieveDestroyAPIView):
    queryset = CardanoCreateTransaction.objects.all()
    serializer_class = CardanoCreateTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


