from django import forms

COUNTY_CHOICES = [('Nairobi', 'Nairobi')]

class CustomerDetailsForm(forms.Form):
    first_name = forms.CharField(label="First Name*", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Last Name (Optional)", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    county = forms.ChoiceField(label="County*", widget=forms.Select(attrs={'class': 'form-control'}), choices=COUNTY_CHOICES)
    delivery_route = forms.CharField(label="Delivery Route*", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Estate / Local Area Name'}))
    street_address = forms.CharField(label="Street Address*", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Landmark'}))
    additional_description = forms.CharField(label="Additional Description (Optional)", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control','placeholder':'eg. Name of shop or Opposite Naivas supermarket'}))
    phone_number = forms.IntegerField(label="Phone Number*", widget=forms.NumberInput(attrs={'class': 'form-control'}))