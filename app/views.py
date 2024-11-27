from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transactions, Account
from .forms import DepositForm, WithdrawalForm, TransferForm, CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'app/signup.html', {'form':form})

@login_required
def account_details(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transactions.objects.filter(account=account).order_by('-timestamp')
    # Fetching User data (e.g. username or email)
    username = request.user.username
    email = request.user.email
    context = {
        'account':account,
        'transaction':transactions,
        'username': username,
        'email': email,
    }

    return render(request, 'app/account_details.html', context)

@login_required
def deposits(request, account_id):
    print(f"Logged-in user: {request.user.username}")
    account = get_object_or_404(Account, id=account_id, user=request.user)
    print(f"Accessed account: {account}")
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()
            Transactions.objects.create(account=account, transaction_type = 'DP', description=description, amount=amount)
            return redirect('account_details', account_id=account.id)
    else:
        form = DepositForm()
    return render(request, 'app/deposit.html', {'form':form, 'account':account})

@login_required
def withdraw(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    
    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            amount = form.cleaned_data['amount']

            # checking if amount entered is positive
            if amount <= 0:
                messages.error(request, "Please enter a positive withdrawal amount.")
                return render(request, 'app/withdraw.html', {'form': form})

            # checking if amount entered is insufficient
            if amount > account.balance:
                messages.error(request, "Please enter a sufficient withdrawal amount.")
                return render(request, 'app/withdraw.html', {'form': form})

            # deduct amount and save to account
            account.balance -= amount
            account.save()

            # create a transaction record
            Transactions.objects.create(account=account, transaction_type='WD', description=description, amount=amount)

            # return redirect
            return redirect('account_details', account_id=account.id)
    
    # Handle GET request: render the form if the method is GET
    else:
        form = WithdrawalForm()

    return render(request, 'app/withdraw.html', {'form': form, 'account': account})


@login_required
def transfer(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            account_number = form.cleaned_data['account_number']

            #checking is transfer amount is positive
            if amount <= 0:
                messages.error(request, "Sorry, you can't transfer this amount")
                return render(request, 'app/transfer.html', {'form':form, 'account':account})
            
            #checking is balance is suffiencient
            if amount > account.balance:
                messages.error(request, "Insuffucienct Balance")
                return render(request, 'app/transfer.html', {'form':form, 'account':account})
            
            #fetch receipent account through account number
            recepient_account = get_object_or_404(Account, account_number=account_number)

            #deduct amount from user account and add to receipemt's
            account.balance -= amount
            recepient_account.balance += amount
            account.save()
            recepient_account.save()

            #record transactions for both sender and receipent
            Transactions.objects.create(account=account, transaction_type='WD', description=description, amount=amount)
            Transactions.objects.create(account=recepient_account, transaction_type='DP', description=description, amount=amount)

            #redirect to account details page
            return redirect('account_details', account_id=account_id)
    else:
        form = TransferForm()
        
        return render(request, 'app/transfer.html', {'form':form, 'account':account})
    
@login_required
def transactions(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)

    #retrive transaction history of the user
    trasactions = Transactions.objects.filter(account_id=account.id).order_by('-timestamp')

    return render(request, 'app/transaction.html', {'transactions':trasactions, 'account':account})


