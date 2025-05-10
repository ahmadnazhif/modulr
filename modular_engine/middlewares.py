from django.http import Http404
from modular_engine.models import Module

class ModuleInstallMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        slug = self._extract_module_slug(request.path)
        if slug and not self._is_module_installed(slug):
            raise Http404(f"Module '{slug}' is not installed.")
        
        response = self.get_response(request)
        return response

    def _extract_module_slug(self, path):
        """
        Pattern: '/module/<module_slug>/...'
        """
        path_parts = path.split('/')
        if len(path_parts) < 3 or path_parts[1] != 'module':
            return None
        
        return path_parts[2]

    def _is_module_installed(self, slug):
        try:
            module = Module.objects.get(slug=slug)
            return module.is_installed
        except Module.DoesNotExist:
            return False
