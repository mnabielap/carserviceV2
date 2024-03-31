from django.urls import path
from authentication.views import *

app_name = 'authentication'
urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    # path('register/', register, name='register'),
    # path('register_technician/', register_technician, name='register_technician'),
    # path('register_staff/', register_staff, name='register_staff'),
    # path('register_owner/', register_owner, name='register_owner'),
]