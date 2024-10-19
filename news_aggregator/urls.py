# from django.urls import path
# from . import views

# urlpatterns = [
#     path('news/', views.news_list, name='news_list'),
# ]

from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('', views.news_list, name='news_list'),  # Route for the news list
]
