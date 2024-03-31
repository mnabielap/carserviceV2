from django.urls import path
from technician.views import *

app_name = 'technician'
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard_technician'),
    path('create-service-form/',create_service_form, name='create_service_form'),
    path('list-for-edit/',list_for_edit, name='list_for_edit'),
    path('edit-service/<int:service_id>/', edit_service, name='edit_service'),
    path('history-service/', history_service, name='history_service'),
]