from django.contrib import admin
from django.apps import apps
from .models import Purchase

# Get all models from the 'purchases' app
models = apps.get_app_config('purchases').get_models()

# Register each model dynamically
for model in models:
    admin.site.register(model)
