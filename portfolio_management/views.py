from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from order_management.models import Order
from .models import AmountDetails,Portfolio
from .get_current_price import price

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

    
    portfolios = Portfolio.objects.filter(user=request.user)

    instrument_list = [portfolio.instrument for portfolio in portfolios]
    instrument_string = ",".join(instrument_list)
    current_prices = price(instrument_string) 

    # Pass the deposited amount to the template
    context = {
        'cash_left': cash_left,
        'invested_amount':invested_amount,
        'portfolios': portfolios,
        'current_prices':current_prices,
    }
    return render(request,'portifolio.html',context)            



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