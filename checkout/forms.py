from django import forms
<<<<<<< HEAD
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
        
=======
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
>>>>>>> eb922ec0d8a8b03645b914fd5877800b77e1adad
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
<<<<<<< HEAD
            if field != 'country':  # Skip country field
                if self.fields[field].required:
                    placeholder = f'{placeholders.get(field, "")} *'
                else:
                    placeholder = placeholders.get(field, "")
=======
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
>>>>>>> eb922ec0d8a8b03645b914fd5877800b77e1adad
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False