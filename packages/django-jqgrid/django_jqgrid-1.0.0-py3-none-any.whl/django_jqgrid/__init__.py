# Django JQGrid - Easy jqGrid integration for Django
# Version information
__version__ = '1.0.0'

# Lazy imports to avoid AppRegistryNotReady errors
def __getattr__(name):
    if name == 'JQGridAutoConfig':
        from .auto_config import JQGridAutoConfig
        return JQGridAutoConfig
    elif name == 'ModelConfigRegistry':
        from .auto_config import ModelConfigRegistry
        return ModelConfigRegistry
    elif name == 'jqgrid_registry':
        from .auto_config import jqgrid_registry
        return jqgrid_registry
    elif name == 'register_model':
        from .auto_config import register_model
        return register_model
    elif name == 'JQGridMixin':
        from .mixins import JqGridConfigMixin
        return JqGridConfigMixin
    elif name == 'JQGridView':
        from .views import JQGridView
        return JQGridView
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    'JQGridAutoConfig',
    'ModelConfigRegistry', 
    'jqgrid_registry',
    'register_model',
    'JQGridMixin',
    'JQGridView',
    '__version__',
]

# Auto-discover configurations when Django starts
default_app_config = 'django_jqgrid.apps.DjangoJqgridConfig'
