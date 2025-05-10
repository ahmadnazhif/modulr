import importlib
from modular_engine.module_base import BaseModuleInstaller

def run_module_action(module_name, action):
    try:
        mod = importlib.import_module(f"{module_name}.install")
        for attr in dir(mod):
            obj = getattr(mod, attr)
            if isinstance(obj, type) and issubclass(obj, BaseModuleInstaller):
                instance = obj()
                getattr(instance, action)()
                return
        raise RuntimeError(f"No installer class found in '{module_name}.install'")
    except Exception as e:
        raise RuntimeError(f"{action} on {module_name} failed: {e}")
