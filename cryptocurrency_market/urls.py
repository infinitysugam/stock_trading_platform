from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('', views.cryptocurrency_market, name='cryptocurrency_market'),  # Route for the news list
]



