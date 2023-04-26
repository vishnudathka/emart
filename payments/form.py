from django import forms
from .models import Customer

class PaymentForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=10)
    product_id = forms.IntegerField()
    
    def create_customer(self, user):
        customer = Customer.objects.create(user=user)
        customer.create_stripe_customer()
        return customer