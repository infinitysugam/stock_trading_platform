from django.db import models
from django.contrib.auth.models import User



class AmountDetails(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    cash_amount = models.DecimalField(max_digits=50,decimal_places=5)
    used_amount = models.DecimalField(max_digits=50,decimal_places=5)



class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    instrument = models.CharField(max_length=10)
    quantity = models.BigIntegerField(default=0)
    average_price = models.DecimalField(max_digits=10, decimal_places=5,default=0.0)
    stop_loss = models.DecimalField(max_digits=10,decimal_places=5) 
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"



# class PortfolioInstrument(models.Model):
#     portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
#     instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
#     quantity = models.BigIntegerField()
#     average_price = models.DecimalField(max_digits=10, decimal_places=5)  # Weighted average price
#     current_price = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)  # Latest market price
#     last_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.instrument.symbol} in {self.portfolio.name}"

#     def current_value(self):
#         """
#         Calculate the current value of this instrument in the portfolio.
#         """
#         if self.current_price:
#             return self.quantity * self.current_price
#         return 0

#     def unrealized_return(self):
#         """
#         Calculate the unrealized return (profit or loss).
#         """
#         if self.current_price:
#             return (self.current_price - self.average_price) * self.quantity
#         return 0
