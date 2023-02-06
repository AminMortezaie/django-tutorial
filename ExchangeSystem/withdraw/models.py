from django.db import models


class WithdrawRequest(models.Model):
    value = models.FloatField()
    network_type = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    encryption = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"WithdrawRequest(value={self.value}, network_type={self.network_type}, address={self.address}, encryption={self.encryption})"
