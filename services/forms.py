from django import forms
from django.core.exceptions import ValidationError

from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"