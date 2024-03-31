from django.urls import path
from owner.views import *

app_name = 'owner'
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard_owner'),
    path('list-all-service/', list_all_service, name='list_all_service'),
    path('service-detail/<int:service_id>/', service_detail, name='service_detail'),
    path('add-user/', add_user, name='add_user'),
]