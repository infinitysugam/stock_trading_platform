from django.shortcuts import render

# Create your views here.


def forex(request):
    return render(request, 'forex.html')