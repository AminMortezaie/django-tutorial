from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import Response, status
from .models import SenderWallet
from .serializers import SenderWalletSerializer
from cosmospy import BIP32DerivationError, seed_to_privkey
from cosmospy import Transaction


class SenderWalletObject(generics.RetrieveDestroyAPIView):
    serializer_class = SenderWalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SenderWallet.objects.all()

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError("This record is not available.")


class SenderWalletList(generics.ListCreateAPIView):
    queryset = SenderWallet.objects.all()
    serializer_class = SenderWalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
        sender_wallet = SenderWalletSerializer(data=self.request.data)
        if sender_wallet.is_valid():
            seed = sender_wallet.data['seed']
            # bip32_bytes = bitcoin.bip32_key_from_string(seed)
            # seed = base64.b64encode(bip32_bytes)
            # serializer.save(private_key=self.private_key_from_seed(seed))

    def private_key_from_seed(self, seed):
        try:
            private_key = seed_to_privkey(seed, path="m/44'/118'/0'/0/0")
            return private_key
        except BIP32DerivationError:
            raise ValidationError("Your seed is not correct.")