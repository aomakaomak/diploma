from django import forms
from django.core.exceptions import ValidationError

from .models import Appointment, Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ("result", "owner", "user")


class FeedbackForm(forms.Form):
    name = forms.CharField(
        label="Имя",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ваше имя"}
        ),
    )
    phone = forms.CharField(
        label="Телефон",
        max_length=50,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+7 (___) ___-__-__"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "name@example.com"}
        ),
    )
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Напишите, что вас интересует",
            }
        ),
    )

    def clean_message(self):
        msg = self.cleaned_data["message"].strip()
        if len(msg) < 10:
            raise forms.ValidationError("Сообщение должно быть не короче 10 символов.")
        return msg
