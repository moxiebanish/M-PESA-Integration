from .models import Customer, Transaction
from django import forms

class CustomerForm(forms.ModelForm):
    class Meta: 
        model = Customer
        fields = ['name', 'email', 'number']
        widgets = {
            'name': forms.TextInput({'placeholder': 'Enter your name...'}),
            'email': forms.EmailInput({'placeholder': 'Enter your email...'}),
            'number': forms.TextInput({'placeholder': 'Enter your Mpesa number...'})
        }

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']
        widgets = {
            'amount': forms.TextInput({'placeholder': 'Enter the amount you want to pay'})
            }