"""
URL configuration for ispbox_oss project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from user import views as user_views

from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth.decorators import login_required

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('tenant.urls')),
    #users sign up
    path('user/signup/tenant/', user_views.tenant_signup_view, name='tenant-register'),
    # path('user/signup/customer/',user_views.customer_signup_view,name='farmer-register'),

    #users login 
    path('tenant/login/',user_views.tenant_login,name='tenant-login'),
    # path('customer/login/',user_views.farmer_login,name='farmer-login'),

    path('logout/', user_views.user_logout, name='logout'),
]
