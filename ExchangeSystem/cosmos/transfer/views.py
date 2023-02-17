from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import Response, status
from .models import SenderWallet, ReceiverWallet, CreateTransaction, PublishTransaction
from .serializers import SenderWalletSerializer, ReceiverWalletSerializer, CreateTransactionSerializer, PublishTransactionSerializer
from .cosmos_utilities import CosmospyUtilities


class SenderWalletObject(generics.RetrieveDestroyAPIView):
    queryset = SenderWallet.objects.all()
    serializer_class = SenderWalletSerializer
    permission_classes = [permissions.IsAuthenticated]


class SenderWalletList(generics.ListCreateAPIView):
    queryset = SenderWallet.objects.all()
    serializer_class = SenderWalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        sender_wallet = SenderWallet.objects.all()
        seed = list(sender_wallet.values('seed'))[-1]['seed']
        private_key = CosmospyUtilities.private_key_from_seed_for_model(seed)
        serializer.save(private_key=private_key)


class ReceiverWalletList(generics.ListCreateAPIView):
    queryset = ReceiverWallet.objects.all()
    serializer_class = ReceiverWalletSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReceiverWalletObject(generics.RetrieveDestroyAPIView):
    queryset = ReceiverWallet.objects.all()
    serializer_class = ReceiverWalletSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreateTransactionsList(generics.ListCreateAPIView):
    queryset = CreateTransaction.objects.all()
    serializer_class = CreateTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreateTransactionObject(generics.RetrieveDestroyAPIView):
    queryset = CreateTransaction.objects.all()
    serializer_class = CreateTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransactionsList(generics.ListCreateAPIView):
    queryset = PublishTransaction.objects.all()
    serializer_class = PublishTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()
        transaction = PublishTransaction.objects.all()
        self.get_response_from_transfer_request(transaction)
        serializer.save()
        # CosmospyUtilities.request_transfer_api()

    def get_values_from_create_transaction(self, transaction):
        create_transaction_pk = list(transaction.values('create_transaction'))[-1]['create_transaction']
        desire_create_transaction = CreateTransaction.objects.filter(pk=create_transaction_pk)
        desire_create_transaction_values = list(desire_create_transaction.values())
        return {**self.get_values_from_sender_wallet(desire_create_transaction_values[0]['from_address_id']),  **self.get_values_from_receiver_wallet(desire_create_transaction_values[0]['to_address_id'])}

    @staticmethod
    def get_values_from_sender_wallet(sender_wallet_pk):
        sender_wallet = SenderWallet.objects.filter(pk=sender_wallet_pk)
        sender_wallet_values = list(sender_wallet.values())[0]
        return {'from_address': sender_wallet_values['from_address'], "private_key": CosmospyUtilities.decode_private_key_for_request(sender_wallet_values['private_key']),
                "account_number": sender_wallet_values['account_number'], "sequence": sender_wallet_values['sequence']}

    @staticmethod
    def get_values_from_receiver_wallet(receiver_wallet_pk):
        receiver_wallet = ReceiverWallet.objects.filter(pk=receiver_wallet_pk)
        receiver_wallet_values = list(receiver_wallet.values())[0]
        return {"to_address": receiver_wallet_values['to_address'], "memo": receiver_wallet_values['memo']}

    def get_response_from_transfer_request(self, transaction):
        print(self.get_values_from_create_transaction(transaction))





class TransactionObject(generics.RetrieveDestroyAPIView):
    queryset = PublishTransaction.objects.all()
    serializer_class = PublishTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]