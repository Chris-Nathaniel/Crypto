from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from crypto.models import Wallet, Transaction, tokenForm
from decimal import Decimal
from django.contrib.auth import logout
from .helpers import user_authenticated

baseCost = 0.0033

@user_authenticated
def index(request):
    user = request.session.get("user")

    if 'sell' in request.GET:
        request.session["mode"] = 'sell'
    else:
        request.session["mode"] = 'buy'

    wallet = Wallet.objects.filter(session_id=user).exclude(quantity=0).order_by('-quantity')

    return render(request, 'index.html', {'tokenForm': tokenForm(), 'mode': request.session["mode"], 'wallet': wallet, 'session_id': user})

@user_authenticated
def process_token(request):
    global baseCost
    if request.method == 'POST':
        user = request.session.get("user")
        form = tokenForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data["token"]
        mode = 'buy' if 'buy' in request.POST else 'sell'
        fee = 1 + baseCost if mode == 'buy' else 1 - baseCost
        try:
            if mode.lower() == "buy":
                buy_token(form, fee, user)
            else:
                sell_token(form, fee, user)

        except Wallet.DoesNotExist:
            form.add_error("token", f"Token {token} not found in wallet.")
            return render(request, "index.html", {'tokenForm': form})
            
        return redirect("crypto:index")
    
@user_authenticated
def transaction_view(request):
    user = request.session.get("user")
    
    transactions = Transaction.objects.filter(session_id=user).order_by('-date')
    return render(request, 'transaction.html', {'transactions': transactions, 'session_id': user})

@user_authenticated
def wallet_view(request):
    user = request.session.get("user")

    wallet = Wallet.objects.filter(session_id=user).order_by('-quantity')
    return render(request, 'wallet.html', {'wallet': wallet, 'session_id': user})

def buy_token(form, fee, id):
    global baseCost
    if form.is_valid():
        token = form.cleaned_data["token"]
        price = form.cleaned_data["price"]
        amount = form.cleaned_data["amount"]
        quantity = float(amount)/fee/float(price)
    
    transaction = Transaction(session_id=id, token=token.upper(), price=price, transaction_type="buy", amount=amount, quantity=quantity)
    transaction.save()
    wallet, created = Wallet.objects.get_or_create(session_id=id, token=token.upper(), defaults={
    'balance': Decimal(str(amount)),
    'quantity': Decimal(str(quantity)),
    'average_price': round(Decimal(str(amount * (1-baseCost)/ quantity))),
    })

    if not created:
        wallet.quantity += Decimal(str(quantity))
        wallet.balance += Decimal(str(amount))
        wallet.average_price = round(wallet.balance*Decimal(1-baseCost)/wallet.quantity)
        wallet.save()

def sell_token(form, fee, id):
    if form.is_valid():
        token = form.cleaned_data["token"]
        price = Decimal(form.cleaned_data["price"])
        percentageAmount = Decimal(form.cleaned_data["percentage"]) / Decimal('100')
        amount_input = form.cleaned_data.get("amount")
         
        wallet_token = Wallet.objects.get(session_id=id, token=token.upper())
        if amount_input:  
            percentageAmount = Decimal(amount_input) / wallet_token.balance

        fee_decimal = Decimal(str(fee))
        quantitySold = wallet_token.quantity * percentageAmount
        cogs = quantitySold * wallet_token.average_price * Decimal(1 + baseCost)
        revenue = quantitySold * price * fee_decimal
        tradeReturn = round(revenue - cogs, 2) if wallet_token.quantity > 0 else Decimal('0')

        if quantitySold <= wallet_token.quantity:
            transaction = Transaction(session_id=id, token=token.upper(), price=price, transaction_type="sell", amount=revenue, quantity=quantitySold, cogs=cogs)
            transaction.save()
            wallet_token.quantity -= quantitySold
            wallet_token.balance -= cogs if wallet_token.balance > cogs else wallet_token.balance
            wallet_token.average_price = round(wallet_token.balance/Decimal(1+baseCost)/wallet_token.quantity) if wallet_token.quantity > 0 else Decimal('0')
            wallet_token.return_on_investment += tradeReturn
            wallet_token.save()

def delete_transaction(request, id):
    user = request.session.get("user")
    transaction = get_object_or_404(Transaction, id=id, session_id=user)
    wallet = Wallet.objects.get(session_id=user, token=transaction.token)
    
    if transaction.transaction_type == "buy":
        # Check if any sell transaction exists after this buy for the same token and user
        sell_after_buy_exists = Transaction.objects.filter(
            session_id=user,
            token=transaction.token,
            transaction_type="sell",
            date__gt=transaction.date
        ).exists()

        if sell_after_buy_exists:
            messages.error(request, "You can't delete this buy transaction because a sell has already been made after it.")
            return redirect("crypto:transaction")
        
        wallet.balance -= transaction.amount
        wallet.quantity -= transaction.quantity
        wallet.average_price = round(wallet.balance*Decimal(1-baseCost)/wallet.quantity) if wallet.quantity > 0 else Decimal('0')
        wallet.save()
        transaction.delete()

    if transaction.transaction_type == "sell":
        wallet.balance += transaction.cogs
        wallet.quantity += transaction.quantity
        wallet.average_price = round(wallet.balance*Decimal(1-baseCost)/wallet.quantity) if wallet.quantity > 0 else Decimal('0')   
        wallet.return_on_investment -= round(transaction.amount - transaction.cogs)
        wallet.save()
        transaction.delete()

    return redirect("crypto:transaction")

def reset_session(request):
    # clear the current session id
    request.session.flush()
    # create a new session id
    request.session.create()
    return HttpResponseRedirect(reverse("crypto:index"))

def logout_view(request):
    # clear the current session id
    request.session.flush()
    return redirect('crypto:index')