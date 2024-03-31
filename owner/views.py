from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from authentication.models import UserManage
from technician.models import CarService
from utility.util import check_is_completed, generateRandomString
from django.conf import settings
from technician.models import CarService, PartToService
from django.core.mail import send_mail

WEBURL = settings.CSRF_TRUSTED_ORIGINS[0]

@login_required
def dashboard(request):
    username = request.user.username
    context = {'username': username}
    return render(request, 'dashboard_owner.html', context=context)

@login_required
def list_all_service(request):
    context = dict()
    if request.method == 'POST':
        idToRestore = request.POST.get('restore')
        car_service = CarService.objects.get(pk=int(idToRestore))
        car_service.is_deleted = False
        car_service.save()

    if request.user.is_owner:
        car_services = CarService.objects.all()

        rendered_car_services = []
        for car_service in car_services:

            parts_to_service = car_service.part_to_service.all()
            status_now = None
            if check_is_completed(parts_to_service):
                status_now = "Aktif"
            else:
                status_now = "Belum diputuskan"
            if car_service.is_deleted:
                status_now = "Deleted"
            rendered_car_services.append((car_service, car_service.service_date.strftime('%Y-%m-%d'), status_now))
        context['car_services'] = rendered_car_services
        return render(request, 'list_all_service.html', context)
    else:
        return redirect('owner:dashboard_owner')
    
def service_detail(request, service_id):
    car_service = CarService.objects.get(pk=service_id)

    parts_to_service = car_service.part_to_service.all()
    status_complete_before_post = check_is_completed(parts_to_service)

    if request.method == 'POST':
        car_service_id = request.POST.get('car_service_id')
        part_to_service_id = request.POST.get('part_to_service_id')
        reason = request.POST.get('reason')
        action = request.POST.get('action')

        if action == 'approve':
            part_to_service = PartToService.objects.get(pk=part_to_service_id)
            part_to_service.is_approved = True
        elif action == 'reject':
            part_to_service = PartToService.objects.get(pk=part_to_service_id)
            part_to_service.is_rejected = True
        part_to_service.validated_by = request.user.username
        part_to_service.reason = reason
        part_to_service.save()

        car_service = CarService.objects.get(pk=car_service_id)
    
    parts_to_service = car_service.part_to_service.all()

    is_completed = check_is_completed(parts_to_service)

    if (not status_complete_before_post) and (is_completed):
        print(send_mail(
            f"Pesanan Service Mobil Baru ke-{service_id}",
            f"Haloo, Terdapat Pesanan Service Mobil yang telah diputuskan\n\nBerikut merupakan linknya: {WEBURL}staff/generate-pdf/{service_id}/\n\n",
            f"{settings.EMAIL_HOST_USER}",
            recipient_list=["hobimobil.report@gmail.com"],
            fail_silently=False,
        ))

    appended_parts = []
    for part_to_service in parts_to_service:
        try:
            appended_parts.append((part_to_service, str(part_to_service.car_video.url).split("/")[-1]))
        except:
            appended_parts.append((part_to_service, None))

    no_wa_temp = car_service.techinician_phone.strip()
    if no_wa_temp.startswith("0"):
        no_wa_temp = "62" + no_wa_temp[1:]
    whatsapp_link = f'https://api.whatsapp.com/send?phone={no_wa_temp}&text=Haloo%2C%20Terdapat%20Pesanan%20Service%20Mobil%20yang%20telah%20diputuskan%0A%0ABerikut%20merupakan%20linknya%3A%20{WEBURL}staff/generate-pdf/{service_id}%2F%0A%0A'
    
    context = {'car_service': car_service, 'parts_to_service_list':appended_parts, 'is_completed':is_completed, 'whatsapp_link':whatsapp_link}
    return render(request, 'service_detail_owner.html', context)

def add_user(request):
    context = dict()

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        try:
            if role == 'technician':
                user = UserManage.objects.create_user(username=username, password=password)
                user.is_technician = True
            elif role == 'staff_member':
                user = UserManage.objects.create_user(username=username, password=password)
                user.is_staff_member = True
            elif role == 'owner':
                user = UserManage.objects.create_superuser(username=username, email=f"{generateRandomString()}@gmail.com", password=password)
                user.is_owner = True

            user.save()

            context['message_flag'] = 'success'
            context['message'] = f'Sukses menyimpan user "{username}" sebagai {role}'
        except Exception as e:
            context['message_flag'] = 'danger'
            context['message'] = str(e)

    return render(request, 'add_user.html', context)