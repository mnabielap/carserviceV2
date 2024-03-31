from django.urls import path
from staff.views import *

app_name = 'staff'
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard_staff'),
    path('service-approval-list/', service_approval_list, name='service_approval_list'),
    path('service-detail/<int:service_id>/', service_detail, name='service_detail'),
    path('generate-pdf/<int:car_service_id>/', generate_pdf, name='generate_pdf'),
]