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

import room
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('room.urls')),
    # path('api/get_all_rooms/', room_views.get_all_rooms),
    path('api/user/login/', room_views.login),
    path('api/user/info/', room_views.info),
]
