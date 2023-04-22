"""feke URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

from room import views as room_views
from order import views as order_views

import room, order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(room.urls)),
    # path('', include('order.urls')),
    # path('api/get_all_rooms/', room_views.get_all_rooms),
    path('api/get_order_list/', order_views.get_order_list),
    # create_order
    path('api/create_order/', order_views.create_order),
    path('api/delete_order/', order_views.delete_order),
    path('api/update_order/', order_views.update_order),
    path('api/get_today_order_list/', order_views.get_today_order_list),
    
    path('api/user/login/', room_views.login),
    path('api/user/info/', room_views.info),
]
