import importlib
from django.shortcuts import render
from django.http import Http404, HttpResponse

from modular_engine.module_runner import run_module_action
from .models import Module
from django.contrib.auth.decorators import login_required, permission_required


def module_list(request):
    modules = Module.objects.all()
    return render(request, 'modular_engine/module_list.html', {'modules': modules})

@login_required
def module_install(request, module_name):
    try:
        module = Module.objects.get(name=module_name)
        if not module.is_installed:
            run_module_action(module_name, 'install')
            return HttpResponse(f"Module {module_name} installed successfully.")
        return HttpResponse(f"Module {module_name} is already installed.")
    except Module.DoesNotExist:
        raise Http404("Module does not exist.")

@login_required
def module_uninstall(request, module_name):
    try:
        module = Module.objects.get(name=module_name)
        if module.is_installed:
            run_module_action(module_name, 'uninstall')
            return HttpResponse(f"Module {module_name} uninstalled successfully.")
        return HttpResponse(f"Module {module_name} is not installed.")
    except Module.DoesNotExist:
        raise Http404("Module does not exist.")

@login_required
def module_upgrade(request, module_name):
    try:
        module = Module.objects.get(name=module_name)
        if module.is_installed:
            run_module_action(module_name, 'upgrade')
            return HttpResponse(f"Module {module_name} upgraded successfully.")
        return HttpResponse(f"Module {module_name} is not installed.")
    except Module.DoesNotExist:
        raise Http404("Module does not exist.")
