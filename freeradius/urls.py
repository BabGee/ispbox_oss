from django.urls import path
from freeradius.views import *

urlpatterns = [
    path('create_freeradius_virtual_server/', CreateFreeRADIUSVirtualServerView.as_view(), name='create_freeradius_virtual_server_api'),
    path('customer/register/<int:tenant_id>/', CreateUserInRadcheckView.as_view(), name='create_user_radcheck_api'),
    path('customer/login/', LoginWithFreeRADIUSView.as_view(), name='login_freeradius_api'),

]