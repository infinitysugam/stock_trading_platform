from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def portfolio(request):
    return render(request,'portifolio.html')