from django.apps import apps
from django.conf import settings
from django.utils.module_loading import import_string
from django.urls import reverse, NoReverseMatch
from django.http import HttpResponse
from django.shortcuts import redirect
def get_model(setting_name):
    # Dynamically loads a model based on a setting value like 'app_name.ModelName'.
    model_path = getattr(settings, setting_name)
    app_label, model_name = model_path.split('.')
    return apps.get_model(app_label, model_name)

def resolve_redirect(value, result=None):
    """
    Resolves a redirect value. Supports:
    - callable function (dotted path or directly callable)
    - named URL pattern
    - hardcoded URL path
    """
    if not value:
        return redirect('/')

    # If it's a dotted path to a function
    if isinstance(value, str) and '.' in value:
        try:
            func = import_string(value)
            redirect_value = func(result) if result else func()
            return redirect_value if isinstance(redirect_value, HttpResponse) else redirect(redirect_value)
        except Exception as e:
            print("⚠️ Failed to import redirect function:", e)
            return redirect('/')

    # If it's a named URL
    if isinstance(value, str):
        try:
            if result and "order_reference" in result:
                return redirect(reverse(value, kwargs={"order_reference": result["order_reference"]}))
            return redirect(reverse(value))
        except NoReverseMatch:
            print(f"⚠️ Could not reverse URL name: {value}")
            return redirect(value)  # fallback to path string

    # If it's a direct callable
    if callable(value):
        redirect_value = value(result) if result else value()
        return redirect_value if isinstance(redirect_value, HttpResponse) else redirect(redirect_value)

    return value
