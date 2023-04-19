from django.urls import path
from . import views

urlpatterns = [
    path('get_order_list/', views.get_order_list),
]