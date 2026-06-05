from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'shipping_address']
        widgets = {
            'shipping_address': forms.Textarea(attrs={'rows': 3, 'class': 'block w-full rounded-md border-gray-300 shadow-sm'}),
        }