import importlib
from django.conf import settings
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.urls import Resolver404, resolve

from modular_engine.module_runner import run_module_action
from .models import Module
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import redirect


def _has_landing_page(module_slug):
    try:
        resolve(f'/module/{module_slug}/')
        return True
    except Resolver404:
        return False

def module_list(request):
    module_names = Module.objects.all()
    included_ids = []

    for module in module_names:
        if module.name in settings.INSTALLED_APPS and _has_landing_page(module.slug):
            included_ids.append(module.id)

    modules = Module.objects.filter(id__in=included_ids).order_by('name')
    return render(request, 'modular_engine/module_list.html', {'modules': modules})

@login_required
def module_install(request, slug):
    try:
        module = Module.objects.get(slug=slug)
        if not module.is_installed:
            run_module_action(module.name, 'install')
            messages.add_message(request, messages.SUCCESS, f"Module {slug} installed successfully.")
            return redirect('module_list')
        return HttpResponse(f"Module {slug} is already installed.")
    except Module.DoesNotExist:
        raise Http404("Module does not exist.")

@login_required
def module_uninstall(request, slug):
    try:
        module = Module.objects.get(slug=slug)
        if module.is_installed:
            run_module_action(module.name, 'uninstall')
            messages.add_message(request, messages.SUCCESS, f"Module {slug} uninstalled successfully.")
            return redirect('module_list')
    except Module.DoesNotExist:
        raise Http404("Module does not exist.")

@login_required
def module_upgrade(request, slug):
    try:
        module = Module.objects.get(slug=slug)
        if module.is_installed:
            run_module_action(module.name, 'upgrade')
            messages.add_message(request, messages.SUCCESS, f"Module {slug} upgraded successfully.")
            return redirect('module_list')
        return HttpResponse(f"Module {slug} is not installed.")
    except Module.DoesNotExist:
        raise Http404("Module does not exist.")
