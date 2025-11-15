from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['nom', 'telephone', 'adresse', 'mode_livraison']
