from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import render, redirect

def logout_view(request):
    logout(request)
    return redirect('authentication:home')

def play_video(request, filename):
    context = dict()
    context['filename'] = filename
    context['weburl'] = settings.CSRF_TRUSTED_ORIGINS[0]
    return render(request, 'play_video.html', context=context)