"""
Django JQGrid Configuration Module

This module provides centralized configuration for django_jqgrid,
making it DRY, optimized, and highly configurable.
"""
from django.conf import settings
from django.core.signals import setting_changed
from django.utils.functional import LazyObject


class JQGridDefaults:
    """Default configuration values for django_jqgrid"""
    
    # Grid Display Settings
    GRID_HEIGHT = 400
    GRID_WIDTH = 'auto'
    ROW_NUM = 25
    ROW_LIST = [10, 25, 50, 100, 500, 1000]
    MULTISELECT = True
    MULTIBOX_ONLY = True
    
    # UI Settings
    ICON_SET = 'fontAwesome'
    GUI_STYLE = 'bootstrap4'
    LOCALE = 'en'
    
    # Form Settings
    FORM_COLUMNS = 4
    FORM_WIDTH = 800
    FORM_HEIGHT = 'auto'
    
    # Date/Time Formats
    DATE_FORMAT = 'Y-m-d'
    DATETIME_FORMAT = 'Y-m-d H:i:s'
    TIME_FORMAT = 'H:i:s'
    
    # Search Operators by Field Type
    SEARCH_OPERATORS = {
        'text': ['eq', 'ne', 'cn', 'nc', 'bw', 'bn', 'ew', 'en'],
        'number': ['eq', 'ne', 'lt', 'le', 'gt', 'ge'],
        'date': ['eq', 'ne', 'lt', 'le', 'gt', 'ge'],
        'boolean': ['eq', 'ne'],
        'select': ['eq', 'ne', 'in', 'ni'],
    }
    
    # Field Type Mappings
    FIELD_TYPE_MAP = {
        'CharField': 'text',
        'TextField': 'text',
        'EmailField': 'text',
        'URLField': 'text',
        'SlugField': 'text',
        'IntegerField': 'number',
        'FloatField': 'number',
        'DecimalField': 'number',
        'BooleanField': 'boolean',
        'DateField': 'date',
        'DateTimeField': 'date',
        'ForeignKey': 'select',
        'ManyToManyField': 'select',
    }
    
    # Performance Settings
    ENABLE_CACHE = True
    CACHE_TIMEOUT = 300  # 5 minutes
    OPTIMIZE_QUERIES = True
    DEFAULT_PAGE_SIZE = 50
    MAX_PAGE_SIZE = 1000
    
    # Security Settings
    ENABLE_CSRF = True
    FIELD_LEVEL_PERMISSIONS = False
    AUDIT_CHANGES = False
    
    # Plugin Settings
    ENABLE_IMPORT_EXPORT = True
    ENABLE_FILTERS = True
    ENABLE_COLUMN_CHOOSER = True
    ENABLE_FREEZE_COLUMNS = False
    
    # Static Files Configuration
    STATIC_URL_PREFIX = '/static/django_jqgrid/'
    USE_CDN = False
    CDN_BASE_URL = 'https://cdn.jsdelivr.net/npm/'


class JQGridSettings(LazyObject):
    """
    A lazy proxy for django_jqgrid settings, providing both
    defaults and the ability to override from Django settings.
    """
    def _setup(self):
        self._wrapped = Settings()


class Settings:
    """
    Settings class that merges defaults with user settings.
    """
    def __init__(self):
        self.defaults = JQGridDefaults()
        self._cached_attrs = set()
        
    def __getattr__(self, attr):
        if attr not in self._cached_attrs:
            # First check user settings
            user_settings = getattr(settings, 'JQGRID_CONFIG', {})
            value = user_settings.get(attr, getattr(self.defaults, attr, None))
            
            # Cache the value
            setattr(self, attr, value)
            self._cached_attrs.add(attr)
            
        return getattr(self, attr)
    
    def reload(self):
        """Clear cached settings"""
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()


# Create singleton instance
jqgrid_settings = JQGridSettings()


# Listen for settings changes
def reload_settings(*args, **kwargs):
    setting = kwargs.get('setting')
    if setting == 'JQGRID_CONFIG':
        jqgrid_settings._setup()
        

setting_changed.connect(reload_settings)


# Utility functions for common configurations
def get_search_operators(field_type):
    """Get search operators for a field type"""
    field_type_map = jqgrid_settings.FIELD_TYPE_MAP
    search_operators = jqgrid_settings.SEARCH_OPERATORS
    
    base_type = field_type_map.get(field_type, 'text')
    return search_operators.get(base_type, search_operators['text'])


def get_field_config(field_type, **overrides):
    """Get base configuration for a field type"""
    base_configs = {
        'text': {
            'stype': 'text',
            'searchoptions': {'sopt': get_search_operators('text')},
            'edittype': 'text',
            'editrules': {},
        },
        'number': {
            'stype': 'number',
            'searchoptions': {'sopt': get_search_operators('number')},
            'edittype': 'text',
            'editrules': {'number': True},
            'align': 'right',
            'formatter': 'number',
        },
        'boolean': {
            'stype': 'checkbox',
            'searchoptions': {'sopt': get_search_operators('boolean')},
            'edittype': 'checkbox',
            'formatter': 'checkbox',
            'align': 'center',
            'width': 80,
        },
        'date': {
            'stype': 'date',
            'searchoptions': {'sopt': get_search_operators('date')},
            'edittype': 'text',
            'formatter': 'date',
            'formatoptions': {
                'srcformat': 'Y-m-d',
                'newformat': jqgrid_settings.DATE_FORMAT
            },
        },
        'select': {
            'stype': 'select',
            'searchoptions': {'sopt': get_search_operators('select')},
            'edittype': 'select',
            'formatter': 'select',
        }
    }
    
    field_type_map = jqgrid_settings.FIELD_TYPE_MAP
    base_type = field_type_map.get(field_type, 'text')
    config = base_configs.get(base_type, base_configs['text']).copy()
    
    # Apply overrides
    config.update(overrides)
    return config