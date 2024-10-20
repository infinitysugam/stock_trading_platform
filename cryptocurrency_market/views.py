# Create your views here.
from django.shortcuts import render

def cryptocurrency_market(request):
    return render(request, 'cryptocurrency_market.html')  # Render your template for the crypto market



