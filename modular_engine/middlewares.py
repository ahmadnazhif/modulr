from django.http import Http404
from django.shortcuts import render
from modular_engine.models import Module

class ModuleInstallMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        slug = self._extract_module_slug(request.path)
        module = self._get_module(slug) if slug else None
        if module and not module.is_installed:
            return render(request, 'errors/module_not_installed.html', {
                'module': slug
            }, status=403)
        
        response = self.get_response(request)
        return response

    def _extract_module_slug(self, path):
        """
        Pattern: '/module/<module_slug>/...'
        """
        path_parts = path.split('/')
        if len(path_parts) < 3 or path_parts[1] != 'module':
            return None

        if path_parts[2] != 'upgrade':
            return path_parts[2]

        return path_parts[3] if len(path_parts) > 3 else None

    def _get_module(self, slug):
        try:
            return Module.objects.get(slug=slug)
        except Module.DoesNotExist:
            return None
