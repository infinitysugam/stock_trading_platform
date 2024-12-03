from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

from portfolio_management.views import add_notification
from order_management.models import Order
from portfolio_management.models import AmountDetails


from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from decimal import Decimal


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            #messages.success(request, f"Account created for {username}! You can now log in.")
            return redirect('login')  # Replace 'login' with your desired route
        else:
            # Pass the form with errors back to the template
            messages.error(request, "There was an error in your submission. Please check below.")
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('')  # Replace 'home' with your desired URL
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})



def profile(request):
        
        if request.method == 'POST' and 'email' in request.POST:
            # Fetch the user and profile instances
            user = request.user
            profile = user.profile

            # Get the data from the form
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            SSN = request.POST.get('SSN')
            address = request.POST.get('address')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            # Update the user and profile fields
            if email:
                user.email = email
            if phone:
                profile.phone = phone
            if SSN:
                profile.SSN = SSN
            if address:
                profile.address = address
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name

            # Save the changes
            user.save()
            profile.save()

            messages.success(request, 'Your profile has been updated successfully!')

            message = f'''Profile Updated.'''   
            add_notification(request,message)
            return redirect('profile')
        

        if request.method == 'POST' and 'start_date' in request.POST:
            return generate_report(request)
        


                # Handle deposit functionality
        if request.method == 'POST' and 'deposit_amount' in request.POST:
            try:


                deposit, created = AmountDetails.objects.get_or_create(
                user=request.user,
                defaults={'cash_amount': 0, 'used_amount': 0}  # Default values for a new user
            )
                cash_left = deposit.cash_amount if deposit else 0  # Default to 0 if no deposit exists
                invested_amount = deposit.used_amount if deposit else 0

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
                    return redirect('profile')  # Avoid form resubmission
            except Exception as e:
                print(e)
                messages.error(request, "Invalid deposit amount. Please try again.")

        return render(request, 'profile.html', {'user': request.user})




def generate_report(request):
        # Get timeframe from request (e.g., query params)
    start_date = request.POST.get('start_date')  # Expected format: YYYY-MM-DD
    end_date = request.POST.get('end_date')      # Expected format: YYYY-MM-DD


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



@login_required
def logout_view(request):
    logout(request)
    return redirect('login')