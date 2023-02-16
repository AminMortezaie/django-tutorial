from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import Response, status
from .models import SenderWallet
from .serializers import SenderWalletSerializer
from .cosmos_utilities import private_key_from_seed_for_model


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
        sender_wallet = SenderWallet.objects.all()
        seed = list(sender_wallet.values('seed'))[0]['seed']
        private_key = private_key_from_seed_for_model(seed)
        serializer.save(private_key=private_key)