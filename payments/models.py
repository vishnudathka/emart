import stripe
from django.conf import settings
from django.db import models

stripe.api_key = settings.STRIPE_SECRET_KEY


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    description = models.CharField(max_length=255)
    stripe_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} {self.currency} payment on {self.created_at}"