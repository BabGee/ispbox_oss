from django.urls import path
from freeradius.views import *

urlpatterns = [
    path('create_freeradius_virtual_server/', CreateFreeRADIUSVirtualServerView.as_view(), name='create_freeradius_virtual_server_api'),

]