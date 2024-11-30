from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from order_management.models import Order
from .models import AmountDetails,Portfolio,Notification
from .get_current_price import price
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages


# Create your views here.

@login_required
def portfolio(request):
        # Ensure the user is authenticated
    if request.user.is_authenticated:
        # Fetch the deposited amount for the logged-in user
        deposit = AmountDetails.objects.filter(user=request.user).first()
        cash_left = deposit.cash_amount if deposit else 0  # Default to 0 if no deposit exists
        invested_amount = deposit.used_amount if deposit else 0
    else:
        deposited_amount = 0


    
        # Handle deposit functionality
    if request.method == 'POST' and 'deposit_amount' in request.POST:
        try:
            deposit_amount = Decimal(request.POST.get('deposit_amount', 0))
            if deposit_amount <= 0:
                messages.error(request, "Deposit amount must be greater than zero.")
            else:
                deposit.cash_amount += deposit_amount
                deposit.save()
                message = f'''${deposit.amount} Amount Deposited in the platform.'''

                add_notification(request,message)
                messages.success(request, f"Successfully deposited ${deposit_amount:.2f}. Your new balance is ${deposit.cash_amount:.2f}.")
                return redirect('portfolio_management')  # Avoid form resubmission
        except Exception as e:
            messages.error(request, "Invalid deposit amount. Please try again.")

    
    portfolios = Portfolio.objects.filter(user=request.user)

    instrument_list = [portfolio.instrument for portfolio in portfolios]
    instrument_string = ",".join(instrument_list)
    current_prices = price(instrument_string) 

    for portfolio in portfolios:
        current_price = current_prices.get(portfolio.instrument, None)
        portfolio.current_price = Decimal(current_price) if current_price is not None else 'N/A'
        
        # Calculate returns if current price is available
        if current_price is not None and portfolio.average_price:
            portfolio.returns = (Decimal(current_price) - portfolio.average_price) * portfolio.quantity
            portfolio.abs_returns = abs(portfolio.returns)
        else:
            portfolio.returns = 'N/A'
            portfolio.abs_returns = 'N/A'
    # Pass the deposited amount to the template
    context = {
        'cash_left': cash_left,
        'invested_amount':invested_amount,
        'total_amount':cash_left + invested_amount,
        'portfolios': portfolios,
    }
    return render(request,'portifolio.html',context)            





def add_notification(request,message):
    Notification.objects.create(user=request.user,message=message)

@csrf_exempt
def mark_notification_as_seen(request):
    """
    Mark a specific notification as seen.
    """
    
    if request.user.is_authenticated:
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'status': 'unauthorized'}, status=401)

# @login_required
# def combined_view(request):
#     # Fetch orders
#     orders = Order.objects.all().order_by('-timestamp')

#     # Fetch portfolio for the logged-in user (assumes authentication)
#     portfolio = Portfolio.objects.filter(user=request.user).first()
#     portfolio_instruments = []
#     total_portfolio_value = 0

#     if portfolio:
#         portfolio_instruments = portfolio.portfolioinstrument_set.all()
#         total_portfolio_value = portfolio.total_value()

#     # Context for the template
#     context = {
#         'orders': orders,
#         'portfolio': portfolio,
#         'portfolio_instruments': portfolio_instruments,
#         'total_portfolio_value': total_portfolio_value,
#     }
#     return render(request, 'combined_view.html', context)