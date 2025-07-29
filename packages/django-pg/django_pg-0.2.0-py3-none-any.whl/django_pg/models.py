from django.db import models

PAYMENT_METHOD_CHOICES = [
        ('paystack', 'Paystack'),
        ('flutterwave', 'Flutterwave'),
    ]

class BaseOrder(models.Model):
    payment_made = models.BooleanField(default=False)
    order_placed = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="Pending")
    order_reference = models.CharField(max_length=20,)
    payment_method = models.CharField(
        max_length=50, 
        choices=PAYMENT_METHOD_CHOICES,
        blank=True, 
        null=True,
        help_text="The payment gateway used for this order.")
    payment_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
