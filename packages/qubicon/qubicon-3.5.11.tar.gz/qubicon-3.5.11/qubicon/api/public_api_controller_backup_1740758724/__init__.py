"""Auto-import all public API functions from OpenAPI-generated files in public_api_controller_2"""

import pkgutil
import importlib

# Dynamically import all modules in this directory
__all__ = []

for module_info in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f"{__name__}.{module_info.name}")
    globals()[module_info.name] = module
    __all__.append(module_info.name)
