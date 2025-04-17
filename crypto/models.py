from django.db import models
from django import forms

# Create your models here.
class Wallet(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    token = models.CharField(max_length=64)
    balance = models.DecimalField(max_digits=60, decimal_places=0)
    quantity = models.DecimalField(max_digits=60, decimal_places=3)
    average_price = models.DecimalField(max_digits=25, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.token}, {self.balance}, {self.quantity}, {self.average_price}"

class Transaction(models.Model):
    session_id = models.CharField(max_length=255)
    token = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=25, decimal_places=2)
    transaction_type = models.CharField(max_length=25, choices=[("buy", "Buy"), ("sell", "Sell")])
    amount = models.DecimalField(max_digits=25, decimal_places=0)
    quantity = models.DecimalField(max_digits=25, decimal_places=3)  
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.token}, {self.price}, {self.transaction_type}, {self.amount}, {self.quantity}, {self.date}"

class tokenForm(forms.Form):
    token = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter token name'}))
    amount = forms.IntegerField(required=False,widget=forms.NumberInput(attrs={'placeholder': 'Enter amount'}))
    price = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'placeholder': 'Enter price'}))
    percentage = forms.IntegerField(
        required=False,
        initial=0,
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter percentage',
            'type': 'range', 
            'min': 0,
            'max': 100,
            'step': 1, 
            'value': 0 
        })
    )