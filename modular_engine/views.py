from django.shortcuts import render
from .models import Module

def module_list(request):
    modules = Module.objects.all()
    return render(request, 'modular_engine/module_list.html', {'modules': modules})
