from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Account
import random

#deposit form
class DepositForm(forms.Form): #form for deposits
    amount = forms.IntegerField(max_value=10000000, min_value=1)
    description = forms.CharField(max_length=500)

#withdraw form
class WithdrawalForm(forms.Form): #form for withdrawal
    amount = forms.IntegerField(max_value=10000000, min_value=1)
    description = forms.CharField(max_length=500)

#transfer form
class TransferForm(forms.Form):
    account_number = forms.CharField(max_length=12)
    amount = forms.IntegerField(max_value=10000000)
    description = forms.CharField(max_length=500)

#User creation form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email Address')
    first_name = forms.CharField(required=True, label='First Name')
    last_name = forms.CharField(required=True, label='Last Name')

    class Meta:
        model = User  # Now we use the default User model
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email is required.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email


    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']  # Explicitly assign email
        if commit:
            user.save()
            # Create an Account object when the User is created
            Account.objects.create(
                user=user,
                account_number=self.generate_account_number()
            )
        return user


    def generate_account_number(self):
        # You can implement logic to generate a unique account number
        return str(User.objects.count() + 100000)  # Simple example

