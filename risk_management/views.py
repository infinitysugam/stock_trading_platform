from django.shortcuts import render
from portfolio_management.get_current_price import price
from portfolio_management.models import Portfolio
from django.contrib.auth.decorators import login_required
from decimal import Decimal


from order_management.views import automated_trading
from order_management.models import Order
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from portfolio_management.views import add_notification
# Create your views here.

@login_required
def home(request):     
    portfolios = Portfolio.objects.filter(user=request.user)

    orders = Order.objects.filter(user=request.user,order_source='automated').order_by('-timestamp')

    instrument_list = [portfolio.instrument for portfolio in portfolios]
    instrument_string = ",".join(instrument_list)
    current_prices = price(instrument_string) 

    for portfolio in portfolios:
        current_price = current_prices.get(portfolio.instrument, None)
        portfolio.current_price = Decimal(current_price) if current_price is not None else 'N/A'
        
        # Calculate returns if current price is available
        if current_price is not None and portfolio.average_price:
            portfolio.returns = (Decimal(current_price) - portfolio.average_price) * portfolio.quantity
            portfolio.return_percentage = ((Decimal(current_price) - portfolio.average_price) / portfolio.average_price) * 100
            portfolio.abs_return_percentage = abs(portfolio.return_percentage)
            portfolio.abs_returns = abs(portfolio.returns)
        else:
            portfolio.returns = 'N/A'
            portfolio.abs_returns = 'N/A'
            portfolio.return_percentage='N/A'
            portfolio.abs_return_percentage = 'N/A'
    # Pass the deposited amount to the template
    context = {
        'portfolios': portfolios,
        'page_obj':orders,
    }


    for portfolio in portfolios:
        if portfolio.stop_loss!=0 and portfolio.return_percentage<=(-portfolio.stop_loss):
            params={
                'instrument':portfolio.instrument,
                'quantity':portfolio.quantity,
                'price':None,
                'order_type':'sell',
            }
            automated_trading(request,params)


    return render(request,'risk_home.html',context)



@csrf_exempt
def update_stop_loss(request):
    """
    Handle AJAX request to update stop loss values in the database.
    """

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for item in data:
                portfolio = Portfolio.objects.get(id=item['id'], user=request.user)
                portfolio.stop_loss = item['stop_loss']
                portfolio.save()

            message=f"Stop Loss Value Updated for instrument {portfolio.instrument} to {portfolio.stop_loss}%"
            add_notification(request,message)
            return JsonResponse({'success': True, 'message': 'Stop Loss values updated successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})