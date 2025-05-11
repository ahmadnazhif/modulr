from modular_engine.module_base import BaseModuleInstaller

class ProductModuleInstaller(BaseModuleInstaller):
    module_name = "product_module"
    module_slug = "product"

installer = ProductModuleInstaller()
