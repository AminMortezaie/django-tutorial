from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from .models import AllCreateTransaction, AllSenderWallet, AllReceiverWallet
from .serializers import AllCreateTransactionSerializer, AllSenderWalletSerializer, AllReceiverWalletSerializer
from .broadcast_transaction import submit_transaction
import json
from django.core.cache import cache
import requests
import hashlib


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
        transaction_hash = 'No Transaction Accomplished.'
        data = dict(serializer.validated_data)
        print(data)

        try:
            sender_wallet = AllSenderWallet.objects.filter(from_address=data['sender_address'])[0]
        except:
            raise ValidationError("This sender wallet is not Valid. You need to create a new sender wallet!")

        try:
            receiver_wallet = AllReceiverWallet.objects.filter(to_address=data['receiver_address'])[0]
        except:
            raise ValidationError("This receiver wallet is not Valid. You need to create a new receiver wallet!")

        receiver_wallet_data = {'to_address': receiver_wallet.to_address, 'network': receiver_wallet.network,
                                'memo': receiver_wallet.memo}
        payload_network = receiver_wallet_data['network']
        self.network_conflict_error(payload_network, sender_wallet.network, data['network'], data['symbol'])

        if serializer.validated_data['network'] == 'cardano':
            sender_wallet_data = {'from_address': sender_wallet.from_address, 'network': sender_wallet.network,
                                  'private_key': sender_wallet.private_key}
            data.update({'from_address': sender_wallet_data})
            data.update({'from_address': sender_wallet_data, 'to_address': receiver_wallet_data})
            transaction_hash = self.cardano_get_transaction_hash(data)

        elif serializer.validated_data['network'] == 'cosmos':
            sender_wallet_data = {'from_address': sender_wallet.from_address, 'network': sender_wallet.network,
                                  'seed': sender_wallet.private_key}
            data.update({'from_address': sender_wallet_data})
            data.update({'from_address': sender_wallet_data, 'to_address': receiver_wallet_data})
            transaction_hash = self.cosmos_get_transaction_hash(data)

        text = f"['{data['sender_address']}', '{data['receiver_address']}', '{data['amount']}'," \
               f"'{data['symbol'].lower()}','{data['to_address']['memo']}','{data['network'].upper()}', " \
               f"'{transaction_hash}']"

        sample = text + data['midKey'] + str(data['timestamp']) + data['key']
        sha256 = hashlib.sha256()
        sha256.update(sample.encode())
        hashed_value = sha256.hexdigest()
        serializer.save(transaction_hash=hashed_value)

    def cardano_get_values(self, transaction):
        sender_wallet = transaction['from_address']
        receiver_wallet = transaction['to_address']

        return {'from_address': sender_wallet['from_address'],
                "signing_key": sender_wallet['private_key'], "to_address": receiver_wallet['to_address'],
                "amount": transaction['amount']}

    def cardano_get_transaction_hash(self, transaction):
        response = self.cardano_get_values(transaction)
        print("Values Successfully Gathered.")
        tx_hash = submit_transaction(response["from_address"], response["to_address"], response["amount"],
                                     json.dumps(response["signing_key"]))
        if tx_hash == "Balance is insufficient!":
            raise ValidationError("Your balance is insufficient.")
        else:
            return tx_hash

    def cosmos_get_values(self, transaction):
        sender_wallet = transaction['from_address']
        receiver_wallet = transaction['to_address']
        seed = sender_wallet['seed']['seed']

        return {'from_address': sender_wallet['from_address'],
                "seed": seed, "to_address": receiver_wallet['to_address'], "amount": transaction['amount']}

    def cosmos_get_transaction_hash(self, transaction):
        response = self.cosmos_get_values(transaction)
        data = {"from_address": response["from_address"], "to_address": response["to_address"],
                "seed": response["seed"], "amount": response["amount"]}
        headers = {'Content-Type': 'application/json'}
        json_data = json.dumps(data)
        print(data)
        response = requests.post('http://ts:3000/api/broadcast-transaction/', data=json_data, headers=headers)
        data = response.json()
        if int(data['message']['code']) == 0 and response.status_code == 201:
            return data['message']['transactionHash']
        elif int(data['message']['code']) == 5:
            raise ValidationError("Your balance is insufficient.")
        else:
            raise ValidationError('API request failed with status code', response.status_code)

    def network_conflict_error(self, payload_network, second_network, network, symbol):
        if payload_network != second_network:
            raise ValidationError("Sender and receiver networks are not the same.")
        if network != payload_network:
            raise ValidationError("You've entered wrong network.")
        if (network == 'cosmos' and symbol != 'atom') or (network == 'cardano' and symbol != 'ada'):
            raise ValidationError("You've entered wrong Symbol.")
        return "no conflict detected."


class AllCreateTransactionObject(generics.RetrieveDestroyAPIView):
    queryset = AllCreateTransaction.objects.all()
    serializer_class = AllCreateTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
