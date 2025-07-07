from django import forms
from django_countries.fields import CountryField
from .models import Order

class OrderForm(forms.ModelForm):
    country = CountryField(blank_label='Country *').formfield(
        required=True,
        widget=forms.Select(attrs={
            'class': 'stripe-style-input',
        })
    )

    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number', 
                 'town_or_city', 'street_address1',
                'street_address2', 'postcode', 'country', 'county',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':  # Skip country field
                if self.fields[field].required:
                    placeholder = f'{placeholders.get(field, "")} *'
                else:
                    placeholder = placeholders.get(field, "")
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False