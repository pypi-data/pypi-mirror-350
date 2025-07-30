from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .utils import resolve_redirect

SUCCESS_REDIRECT = getattr(settings, 'DJANGO_PG_SUCCESS_REDIRECT', None)
FAILURE_REDIRECT = getattr(settings, 'DJANGO_PG_FAILURE_REDIRECT', None)

@login_required
def payment_verification(request, order_id, payment_method):
    if payment_method == "paystack":
        transaction_id = request.GET.get('reference')
    elif payment_method == "flutterwave":
        transaction_id = request.GET.get('transaction_id')
    else:
        messages.error(request, "Unsupported payment method")
        return redirect(resolve_redirect(FAILURE_REDIRECT))

    from .payment import verify_payment
    result = verify_payment(order_id, transaction_id, request.user, payment_method)

    if result.get("success"):
        return resolve_redirect(SUCCESS_REDIRECT, result)
    else:
        messages.error(request, result.get("message", "Payment verification failed"))
        return redirect(resolve_redirect(FAILURE_REDIRECT, result))
