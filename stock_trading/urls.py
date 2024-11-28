"""
URL configuration for stock_trading project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from market_overwatch import views as market_overwatch_views
from django.contrib.auth import views as auth_views
from users import views as user_views
from order_management import views as order_views
from portfolio_management import views as portfolio_views
from risk_management import views as risk_views
from algorithmic_trading import views as algo_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',market_overwatch_views.trading_view,name='trading_view'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),
    path('register/',user_views.register,name='register'),
    path('order_management/',order_views.order_book_view,name='order_management'),
    path('profile/',user_views.profile,name='profile'),
    path('portfolio_management/',portfolio_views.portfolio,name='portfolio_management'),
    path('risk_management/',risk_views.home,name='risk_management'),
    path('algorithmic_trading/',algo_views.home,name='algorithmic_trading')
]
