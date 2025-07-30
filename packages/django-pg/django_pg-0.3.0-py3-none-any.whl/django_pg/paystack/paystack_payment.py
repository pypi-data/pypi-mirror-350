import requests
from django.utils import timezone
from django.conf import settings
from ..utils import get_model

def verify_paystack_payment(order_id, transaction_id, user):
    # Validate user authentication
    if not user.is_authenticated:
        return {
            "success": False,
            "message": "User must be authenticated to verify payment."
        }

    # Validate user email
    if not user.email:
        return {
            "success": False,
            "message": "User must have a valid email address for payment verification."
        }
    # Get configured Order and Cart models
    Order = get_model('PAYMENT_ORDER_MODEL')

    # Verify the payment with Paystack
    url = f"https://api.paystack.co/transaction/verify/{transaction_id}"
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    result = requests.get(url, headers=headers).json()

    # If Paystack confirms a successful transaction
    if result.get("status") and result["data"]["status"] == "success":
        # Update the order
        order = Order.objects.get(id=order_id)
        order.payment_made = True
        order.order_placed = True
        order.status = "Order Placed"
        order.payment_method = 'paystack'
        order.payment_date = timezone.now()
        order.save()

        return {
            "success": True,
            "order_reference": order.order_reference
        }

    # If verification failed
    return {
        "success": False,
        "message": "Payment verification failed"
    }
