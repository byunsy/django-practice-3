from django import forms
from .models import Product


class RegisterForm(forms.Form):

    prod_name = forms.CharField(
        max_length=128,
        label='Product Name',
        error_messages={
            'required': 'Please tell us the name of the product.'
        }
    )

    prod_price = forms.IntegerField(
        label='Product Price',
        error_messages={
            'required': 'Please select a price for the product.'
        }
    )

    description = forms.CharField(
        label='Product Description',
        error_messages={
            'required': 'Please tell us about the product.'
        }
    )

    prod_stock = forms.IntegerField(
        label='Current Stock',
        error_messages={
            'required': 'Please tell us about the current stock.'
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('prod_name')
        price = cleaned_data.get('prod_price')
        description = cleaned_data.get('description')
        stock = cleaned_data.get('prod_stock')

        if not (name and price and description and stock):
            self.add_error('name', 'Please fill in all the required fields.')
