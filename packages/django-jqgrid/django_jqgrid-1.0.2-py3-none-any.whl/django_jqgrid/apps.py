from django.apps import AppConfig
from django.conf import settings


class DjangoJqgridConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_jqgrid'
    verbose_name = 'Django jqGrid'
    
    def ready(self):
        """Auto-discover models when Django starts"""
        # Only autodiscover if enabled in settings
        if getattr(settings, 'JQGRID_AUTODISCOVER', True):
            from .auto_config import jqgrid_registry
            
            # Get apps to exclude from settings or use defaults
            exclude_apps = getattr(settings, 'JQGRID_EXCLUDE_APPS', [
                'django.contrib.admin',
                'django.contrib.contenttypes', 
                'django.contrib.sessions',
                'django.contrib.auth',
                'django.contrib.messages',
                'django.contrib.staticfiles',
            ])
            
            # Auto-discover models
            jqgrid_registry.autodiscover(exclude_apps=exclude_apps)
