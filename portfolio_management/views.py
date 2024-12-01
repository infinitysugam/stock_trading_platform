from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from order_management.models import Order
from .models import AmountDetails,Portfolio,Notification
from .get_current_price import price
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.contrib import messages

from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse



# Create your views here.

@login_required
def portfolio(request):
        # Ensure the user is authenticated

    #deposit = AmountDetails.objects.filter(user=request.user).first()

    deposit, created = AmountDetails.objects.get_or_create(
    user=request.user,
    defaults={'cash_amount': 0, 'used_amount': 0}  # Default values for a new user
)
    cash_left = deposit.cash_amount if deposit else 0  # Default to 0 if no deposit exists
    invested_amount = deposit.used_amount if deposit else 0



    
        # Handle deposit functionality
    if request.method == 'POST' and 'deposit_amount' in request.POST:
        try:
            deposit_amount = Decimal(request.POST.get('deposit_amount', 0))
            print(deposit_amount)
            if deposit_amount <= 0:
                messages.error(request, "Deposit amount must be greater than zero.")
            else:
                deposit.cash_amount += deposit_amount
                deposit.save()
                message = f'''${deposit_amount} Amount Deposited in the platform.'''

                add_notification(request,message)
                messages.success(request, f"Successfully deposited ${deposit_amount:.2f}. Your new balance is ${deposit.cash_amount:.2f}.")
                return redirect('portfolio_management')  # Avoid form resubmission
        except Exception as e:
            print(e)
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




def generate_report(request):
        # Get timeframe from request (e.g., query params)
    start_date = request.GET.get('start_date')  # Expected format: YYYY-MM-DD
    end_date = request.GET.get('end_date')      # Expected format: YYYY-MM-DD
    
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
        end_date = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
    except ValueError:
        return HttpResponse("Invalid date format. Use YYYY-MM-DD.", status=400)
    
    # Filter orders within the timeframe
    orders = Order.objects.filter(user=request.user)
    if start_date:
        orders = orders.filter(timestamp__gte=start_date)
    if end_date:
        orders = orders.filter(timestamp__lte=end_date)
    
    # Create the PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="orders_report_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf"'

    # Generate PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle("Order Report")

    # Header
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(200, 750, "Order Report")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 730, f"User: {request.user.username}")
    pdf.drawString(50, 710, f"Date Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if start_date:
        pdf.drawString(50, 690, f"Start Date: {start_date.strftime('%Y-%m-%d')}")
    if end_date:
        pdf.drawString(50, 670, f"End Date: {end_date.strftime('%Y-%m-%d')}")

    # Table Header
    y_position = 640
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y_position, "Order ID")
    pdf.drawString(150, y_position, "Instrument")
    pdf.drawString(250, y_position, "Order Type")
    pdf.drawString(350, y_position, "Quantity")
    pdf.drawString(450, y_position, "Price")
    pdf.drawString(520, y_position, "Timestamp")

    # Order Data
    y_position -= 20
    pdf.setFont("Helvetica", 10)
    for order in orders:
        pdf.drawString(50, y_position, str(order.id))
        pdf.drawString(150, y_position, order.instrument)
        pdf.drawString(250, y_position, order.order_type.capitalize())
        pdf.drawString(350, y_position, str(order.quantity))
        pdf.drawString(450, y_position, f"${Decimal(order.price):.2f}")
        pdf.drawString(520, y_position, order.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
        y_position -= 20

        # Add a new page if space is insufficient
        if y_position < 50:
            pdf.showPage()
            y_position = 750

    # Finalize and close PDF
    pdf.save()

    return response