from django.apps import apps
from django.conf import settings

def get_model(setting_name):
    # Dynamically loads a model based on a setting value like 'app_name.ModelName'.
    model_path = getattr(settings, setting_name)
    app_label, model_name = model_path.split('.')
    return apps.get_model(app_label, model_name)
