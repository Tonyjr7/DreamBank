from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model): #Account infos
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    account_type = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

class Transactions(models.Model):
    DEPOSIT = 'DP'
    WITHDRAWAL = 'WD'

    TRANSACTION_TYPE_CHOICES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=2,
        choices=TRANSACTION_TYPE_CHOICES,
        default=DEPOSIT
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.transaction_type

