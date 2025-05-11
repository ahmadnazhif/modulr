import importlib
from modular_engine.module_base import BaseModuleInstaller

def run_module_action(module_name, action):
    try:
        mod = importlib.import_module(f"{module_name}.install")
        obj = getattr(mod, "installer", None)
        if isinstance(obj, BaseModuleInstaller):
            getattr(obj, action)()
            return
        raise RuntimeError(f"No installer class found in '{module_name}.install'")
    except Exception as e:
        raise RuntimeError(f"{action} on {module_name} failed: {e}")
