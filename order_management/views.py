from django.shortcuts import render

def home(request):
        return render(request,'order_home.html')