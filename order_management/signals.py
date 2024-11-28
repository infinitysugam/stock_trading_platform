from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import Order
from portfolio_management.models import Portfolio

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
    order_price = instance.price
    filled_quantity = instance.filled_quantity

    # Only update portfolio for filled or partially filled orders
    if instance.status in ['filled', 'partially_filled']:
        portfolio, created = Portfolio.objects.get_or_create(
            user=user,
            instrument=instrument,
        )

        if order_type == 'buy':
            # Weighted average price formula for buy orders
            total_quantity = portfolio.quantity + filled_quantity
            portfolio.average_price = (
                (portfolio.quantity * portfolio.average_price) +
                (filled_quantity * order_price)
            ) / total_quantity
            portfolio.quantity = total_quantity

        elif order_type == 'sell':
            # Deduct quantity for sell orders
            portfolio.quantity -= filled_quantity
            # Prevent negative quantity
            if portfolio.quantity < 0:
                portfolio.quantity = 0
                portfolio.average_price = 0  # Reset average price if no holdings

        print(portfolio.quantity)

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
