from django import forms
from .models import Order
from product.models import Product
from user.models import User
from django.db import transaction


class OrderForm(forms.Form):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    product = forms.IntegerField(
        label="Product Name",
        widget=forms.HiddenInput
    )

    quantity = forms.IntegerField(
        label='Order Quantity: ',
        error_messages={
            'required': 'Please select a quantity to order.'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        user = self.request.session.get('user')

        if not (product and quantity and user):
            self.add_error('quantity', 'Please select a quantity to order.')
            self.add_error('product', 'Please select a product to order.')

        elif quantity is None:
            self.product = product
            self.add_error('quantity', 'Please select a valid quantity.')

        elif quantity <= 0:
            self.product = product
            self.add_error('quantity', 'Please select a valid quantity.')
