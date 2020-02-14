#———————————————————————————————————————— robots.txt

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

def LabView(request):
    template = 'svija/lab.html' 
    msg = 'message working'

    context = {
        'msg'       : msg
    }

    return render(request, template, context)

#———————————————————————————————————————— fin
