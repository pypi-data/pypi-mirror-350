import requests
from django.utils import timezone
from django.conf import settings
from ..utils import get_model  

def verify_flutterwave_payment(order_id, transaction_id, user):
    if not user.is_authenticated:
        return {
            "success": False,
            "message": "User must be authenticated to verify payment."
        }

    if not user.email:
        return {
            "success": False,
            "message": "User must have a valid email address for payment verification."
        }

    Order = get_model('PAYMENT_ORDER_MODEL')

    url = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.FLUTTERWAVE_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        result = response.json()

        if result.get("status") == "success" and result["data"]["status"] == "successful":
            order = Order.objects.get(id=order_id)
            order.payment_made = True
            order.order_placed = True
            order.status = "Order Placed"
            order.payment_method = 'flutterwave'
            order.payment_date = timezone.now()
            order.save()

            return {
                "success": True,
                "order_reference": order.order_reference
            }

        # Add more detail from the Flutterwave response if available
        error_message = result.get("message", "Unknown error during payment verification.")

        return {
            "success": False,
            "message": f"Payment verification failed: {error_message}"
        }

    except requests.RequestException as e:
        print("❌ Request error while verifying Flutterwave payment:", str(e))
        return {
            "success": False,
            "message": "Error connecting to Flutterwave for verification."
        }
