from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def trading_view(request):
        return render(request,'trading_view.html')