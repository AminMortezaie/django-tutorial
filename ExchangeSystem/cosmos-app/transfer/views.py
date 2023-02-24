from rest_framework import generics, permissions
from .models import SenderWallet, ReceiverWallet, CreateTransaction
from .serializers import SenderWalletSerializer, ReceiverWalletSerializer, CreateTransactionSerializer
import requests
import json


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

    def perform_create(self, serializer):
        transaction_hash = self.get_response_from_transfer_request(serializer.validated_data)
        serializer.save(transaction_hash=transaction_hash, transaction_link="https://explorer.theta-testnet.polypore.xyz/transactions/"+transaction_hash)

    def get_values(self, transaction):
        sender_wallet = transaction['from_address']
        receiver_wallet = transaction['to_address']

        return {'from_address': sender_wallet.from_address,
                "seed": sender_wallet.seed, "to_address": receiver_wallet.to_address, "amount": transaction['amount']}

    def get_response_from_transfer_request(self, transaction):
        response = self.get_values(transaction)
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


class CreateTransactionObject(generics.RetrieveDestroyAPIView):
    queryset = CreateTransaction.objects.all()
    serializer_class = CreateTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]


