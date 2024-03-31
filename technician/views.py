import datetime
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from utility.util import check_is_completed
from .models import CarService, PartToService
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.shortcuts import get_object_or_404

@login_required
def dashboard(request):
    username = request.user.username
    context = {'username': username}
    return render(request, 'dashboard_technician.html', context=context)

@login_required
def create_service_form(request):
    if request.method == 'POST':
        num_parts = int(request.POST.get('num_parts', 1))  # Ambil jumlah parts yang ingin dibuat, defaultnya 1

        license_plate = request.POST.get('license_plate')
        brand = request.POST.get('brand')
        techinician_name = request.POST.get('staff_service_name')
        techinician_phone = request.POST.get('phone_number')
        service_date = request.POST.get('tanggal')

        print(f"service_date: {service_date}")
        car_service = CarService.objects.create(
            user=request.user,
            license_plate=license_plate,
            brand=brand,
            service_date=datetime.datetime.strptime(service_date, '%Y-%m-%d'),
            techinician_name=techinician_name,
            techinician_phone=techinician_phone,
        )

        # Simpan PartToService berdasarkan jumlah yang diinginkan
        for i in range(num_parts):
            part_to_service_text = request.POST.get(f'part_to_service_{i}')
            car_photo = request.FILES.get(f'car_photo_{i}')
            car_video = request.FILES.get(f'car_video_{i}')

            if part_to_service_text:
                if not car_video:
                    part_to_service = PartToService(
                        id_order = i,
                        car_service=car_service,
                        parts_to_service=part_to_service_text,
                        car_photo=car_photo
                    )
                else:
                    part_to_service = PartToService(
                        id_order = i,
                        car_service=car_service,
                        parts_to_service=part_to_service_text,
                        car_photo=car_photo,
                        car_video=car_video
                    )
                part_to_service.save()

        return render(request, 'create_service_form.html', {'status': 'success'})
    else:
        return render(request, 'create_service_form.html')

@login_required
def list_for_edit(request):
    context = dict()
    if request.user.is_technician:
        selected = []
        car_services = CarService.objects.filter(user=request.user)

        for car_service in car_services:
            if car_service.is_deleted:
                continue
            parts_to_service = car_service.part_to_service.all()
            if not check_is_completed(parts_to_service):
                selected.append(car_service)

        context = {'car_services': selected}
        return render(request, 'list_for_edit.html', context)
    else:
        return redirect('technician:dashboard_technician')
    
@login_required
def history_service(request):
    context = dict()
    if request.user.is_technician:
        selected = []
        car_services = CarService.objects.filter(user=request.user)

        for car_service in car_services:
            if car_service.is_deleted:
                continue
            parts_to_service = car_service.part_to_service.all()
            if check_is_completed(parts_to_service):
                selected.append((car_service, "Aktif"))
            else:
                selected.append((car_service, "Belum diputuskan"))

        context['car_services'] = selected
        return render(request, 'history_service.html', context)
    else:
        return redirect('technician:dashboard_technician')
    
@login_required
def edit_service(request, service_id):
    context = dict()
    if request.user.is_technician and request.method == 'POST':
        car_service = CarService.objects.get(pk=service_id)

        num_parts = int(request.POST.get('num_parts', 1))

        license_plate = request.POST.get('license_plate')
        brand = request.POST.get('brand')
        techinician_name = request.POST.get('staff_service_name')
        techinician_phone = request.POST.get('phone_number')
        service_date = request.POST.get('tanggal')

        if car_service.license_plate != license_plate:
            car_service.license_plate = license_plate
        if car_service.brand != brand:
            car_service.brand = brand
        if car_service.techinician_name != techinician_name:
            car_service.techinician_name = techinician_name
        if car_service.techinician_phone != techinician_phone:
            car_service.techinician_phone = techinician_phone
        if car_service.service_date != service_date:
            car_service.service_date = service_date
        car_service.save()

        for i in range(num_parts):
            part_to_service_text = request.POST.get(f'part_to_service_{i}')
            car_photo = request.FILES.get(f'car_photo_{i}')
            car_video = request.FILES.get(f'car_video_{i}')
            try:
                part_to_service = PartToService.objects.get(car_service=car_service, id_order=i)
                if part_to_service.parts_to_service != part_to_service_text:
                    part_to_service.parts_to_service = part_to_service_text
                if car_photo:
                    part_to_service.car_photo = car_photo
                if car_video:
                    part_to_service.car_video = car_video
                part_to_service.save()
            except:
                part_to_service = PartToService(
                    id_order = i,
                    car_service=car_service,
                    parts_to_service=part_to_service_text,
                    car_photo=car_photo if car_photo else None,
                    car_video=car_video if car_video else None,
                )
                part_to_service.save()

        for part_service in car_service.part_to_service.all():
            if part_service.id_order > num_parts-1:
                part_service.delete()

        context['status'] = 'success'

    if request.user.is_technician:
        car_service = CarService.objects.get(pk=service_id)
        parts_to_service = car_service.part_to_service.all()
        context['car_service'] = car_service
        context['converted_date'] = car_service.service_date.strftime('%Y-%m-%d')
        context['parts_to_service'] = parts_to_service
        text_name = []
        enum_parts = []
        for i, part in enumerate(parts_to_service):
            text_name.append(part.parts_to_service)
            enum_parts.append((i, i+1, part))
        context['text_name'] = text_name
        context['enum_parts'] = enum_parts
        context['len_parts_to_service'] = len(parts_to_service)
        return render(request, 'edit_service.html', context)
    else:
        return redirect('technician:dashboard_technician')

@login_required
def test_play_video(request):
    return render(request, 'test_play_video.html')