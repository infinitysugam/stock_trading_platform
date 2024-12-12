from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Order
from portfolio_management.models import Portfolio,AmountDetails

from django.contrib.auth.models import User


from decimal import Decimal
from users.models import Profile

import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Order)
def update_portfolio(sender, instance, **kwargs):
    """
    Update the portfolio whenever an order is made.
    """

    user = instance.user
    instrument = instance.instrument
    order_type = instance.order_type
    order_quantity = instance.quantity
    order_price = Decimal(instance.price)
    filled_quantity = Decimal(instance.filled_quantity)
    total_cost = order_price * filled_quantity

    # Only update portfolio for filled or partially filled orders
    if instance.status in ['filled', 'partially_filled']:


        amount_details, created = AmountDetails.objects.get_or_create(
        user=user,
        defaults={'cash_amount': 0, 'used_amount': 0}
    )
        portfolio, created = Portfolio.objects.get_or_create(
            user=user,
            instrument=instrument,
            defaults={'quantity': 0, 'average_price': Decimal(0.0),'stop_loss':Decimal(0.0)}
        )


        if order_type == 'buy':
            # Weighted average price formula for buy orders
            total_quantity = portfolio.quantity + filled_quantity
            portfolio.average_price = (
                (Decimal(portfolio.quantity) * portfolio.average_price) +
                (filled_quantity * order_price)
            ) / total_quantity
            portfolio.quantity = total_quantity


            amount_details.cash_amount -= total_cost
            amount_details.used_amount += total_cost

        elif order_type == 'sell':
            # Deduct quantity for sell orders
            portfolio.quantity -= filled_quantity
            # Prevent negative quantity


            print("######################################")
            print(portfolio.quantity,filled_quantity)
            if portfolio.quantity <= 0:
                portfolio.delete()  # Delete portfolio if quantity is 0
            else:
                portfolio.average_price = Decimal(0.0)  # Reset average price if no holdings

            amount_details.cash_amount += total_cost
            
            temp = amount_details.used_amount-total_cost
            if temp>0:
                print("###############>0")
                amount_details.used_amount -= total_cost
            else:
                print("##############<0")
                amount_details.used_amount=0
                amount_details.cash_amount -= abs(temp)


        #print(portfolio.quantity)

        amount_details.save()


        if portfolio.id:
            portfolio.save()





@receiver(post_delete, sender=Order)
def remove_from_portfolio(sender, instance, **kwargs):
    """
    Update portfolio when an order is deleted.
    """
    user = instance.user
    instrument = instance.instrument

    try:
        portfolio = Portfolio.objects.get(user=user, instrument=instrument)
        if portfolio.quantity <= 0:
            portfolio.delete()  # Remove portfolio if no quantity remains
    except Portfolio.DoesNotExist:
        pass



@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save() 