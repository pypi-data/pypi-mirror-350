"""
Django JQGrid Auto-Configuration System

This module provides automatic configuration for Django models to work with jqGrid.
"""

from django.apps import apps
from django.conf import settings
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
import json
from typing import Dict, List, Any, Optional, Type


class JQGridAutoConfig:
    """
    Automatic configuration generator for Django models to use with jqGrid
    """
    
    def __init__(self, model: Type[models.Model], **kwargs):
        self.model = model
        self.meta = model._meta
        self.options = kwargs
        self._config = None
        
    @property
    def config(self) -> Dict[str, Any]:
        """Get or generate the jqGrid configuration"""
        if self._config is None:
            self._config = self.generate_config()
        return self._config
        
    def generate_config(self) -> Dict[str, Any]:
        """Generate complete jqGrid configuration for the model"""
        config = {
            'model': f'{self.meta.app_label}.{self.meta.model_name}',
            'url': self.get_url(),
            'datatype': 'json',
            'mtype': 'GET',
            'colModel': self.generate_col_model(),
            'colNames': self.generate_col_names(),
            'rowNum': self.options.get('rowNum', 20),
            'rowList': self.options.get('rowList', [10, 20, 30, 50, 100]),
            'pager': True,
            'sortname': self.get_default_sort_field(),
            'viewrecords': True,
            'sortorder': 'asc',
            'caption': str(self.meta.verbose_name_plural),
            'autowidth': True,
            'height': 'auto',
            'multiselect': self.options.get('multiselect', True),
            'multiboxonly': self.options.get('multiboxonly', True),
            'loadonce': self.options.get('loadonce', False),
            'editurl': self.get_edit_url(),
            'toolbar': [True, "top"],
            'toolbarfilter': True,
        }
        
        # Add custom options
        config.update(self.options.get('jqgrid_options', {}))
        
        return config
        
    def generate_col_model(self) -> List[Dict[str, Any]]:
        """Generate colModel configuration for all fields"""
        col_model = []
        
        # Add ID field first
        col_model.append({
            'name': 'id',
            'index': 'id',
            'key': True,
            'editable': False,
            'width': 60,
            'sorttype': 'int',
            'search': True,
            'searchoptions': {'sopt': ['eq', 'ne', 'lt', 'le', 'gt', 'ge']},
        })
        
        # Process model fields
        for field in self.meta.get_fields():
            if field.concrete and not field.many_to_many and field.name != 'id':
                col_config = self.generate_field_config(field)
                if col_config:
                    col_model.append(col_config)
                    
        return col_model
        
    def generate_col_names(self) -> List[str]:
        """Generate column names for the grid"""
        col_names = ['ID']
        
        for field in self.meta.get_fields():
            if field.concrete and not field.many_to_many and field.name != 'id':
                col_names.append(str(field.verbose_name))
                
        return col_names
        
    def generate_field_config(self, field: models.Field) -> Optional[Dict[str, Any]]:
        """Generate jqGrid column configuration for a specific field"""
        # Skip certain field types
        if isinstance(field, (models.ManyToManyField, models.ManyToOneRel)):
            return None
            
        config = {
            'name': field.name,
            'index': field.name,
            'editable': field.editable and not field.primary_key,
            'sortable': True,
            'search': True,
        }
        
        # Field type specific configuration
        if isinstance(field, models.CharField):
            config.update({
                'edittype': 'text',
                'searchoptions': {'sopt': ['eq', 'ne', 'bw', 'bn', 'ew', 'en', 'cn', 'nc']},
                'editrules': {'required': not field.blank},
            })
            if field.max_length:
                config['editoptions'] = {'maxlength': field.max_length}
                
        elif isinstance(field, models.TextField):
            config.update({
                'edittype': 'textarea',
                'searchoptions': {'sopt': ['cn', 'nc', 'bw', 'bn', 'ew', 'en']},
                'editrules': {'required': not field.blank},
                'width': 200,
            })
            
        elif isinstance(field, models.IntegerField):
            config.update({
                'edittype': 'text',
                'sorttype': 'int',
                'searchoptions': {'sopt': ['eq', 'ne', 'lt', 'le', 'gt', 'ge']},
                'editrules': {'number': True, 'required': not field.blank},
                'align': 'right',
                'formatter': 'integer',
            })
            
        elif isinstance(field, (models.FloatField, models.DecimalField)):
            config.update({
                'edittype': 'text',
                'sorttype': 'float',
                'searchoptions': {'sopt': ['eq', 'ne', 'lt', 'le', 'gt', 'ge']},
                'editrules': {'number': True, 'required': not field.blank},
                'align': 'right',
                'formatter': 'number',
            })
            
        elif isinstance(field, models.BooleanField):
            config.update({
                'edittype': 'checkbox',
                'formatter': 'checkbox',
                'editoptions': {'value': 'true:false'},
                'searchoptions': {'sopt': ['eq']},
                'align': 'center',
                'width': 80,
            })
            
        elif isinstance(field, models.DateField):
            config.update({
                'edittype': 'text',
                'formatter': 'date',
                'formatoptions': {'srcformat': 'Y-m-d', 'newformat': 'Y-m-d'},
                'searchoptions': {'sopt': ['eq', 'ne', 'lt', 'le', 'gt', 'ge']},
                'editoptions': {
                    'dataInit': 'function(elem){$(elem).datepicker({dateFormat:"yy-mm-dd"});}'
                },
                'width': 100,
            })
            
        elif isinstance(field, models.DateTimeField):
            config.update({
                'edittype': 'text',
                'formatter': 'date',
                'formatoptions': {'srcformat': 'Y-m-d H:i:s', 'newformat': 'Y-m-d H:i:s'},
                'searchoptions': {'sopt': ['eq', 'ne', 'lt', 'le', 'gt', 'ge']},
                'width': 150,
            })
            
        elif isinstance(field, models.EmailField):
            config.update({
                'edittype': 'text',
                'searchoptions': {'sopt': ['eq', 'ne', 'bw', 'bn', 'ew', 'en', 'cn', 'nc']},
                'editrules': {'email': True, 'required': not field.blank},
                'formatter': 'email',
            })
            
        elif isinstance(field, models.URLField):
            config.update({
                'edittype': 'text',
                'searchoptions': {'sopt': ['eq', 'ne', 'bw', 'bn', 'ew', 'en', 'cn', 'nc']},
                'editrules': {'url': True, 'required': not field.blank},
                'formatter': 'link',
            })
            
        elif isinstance(field, models.ForeignKey):
            config.update({
                'edittype': 'select',
                'formatter': 'select',
                'searchoptions': {'sopt': ['eq', 'ne']},
                'editoptions': {
                    'dataUrl': self.get_select_url(field),
                    'buildSelect': 'function(data){return "<select>" + data + "</select>";}',
                },
            })
            
        # Handle choice fields
        if hasattr(field, 'choices') and field.choices:
            choices_dict = {str(k): str(v) for k, v in field.choices}
            config.update({
                'edittype': 'select',
                'formatter': 'select',
                'editoptions': {'value': choices_dict},
                'searchoptions': {'sopt': ['eq', 'ne'], 'value': choices_dict},
            })
            
        # Set default width based on field type
        if 'width' not in config:
            if isinstance(field, (models.CharField, models.EmailField, models.URLField)):
                config['width'] = min(150, (field.max_length or 150) * 7)
            else:
                config['width'] = 100
                
        return config
        
    def get_url(self) -> str:
        """Get the data URL for the grid"""
        return self.options.get('url', f'/api/{self.meta.app_label}/{self.meta.model_name}/')
        
    def get_edit_url(self) -> str:
        """Get the edit URL for the grid"""
        return self.options.get('edit_url', f'/api/{self.meta.app_label}/{self.meta.model_name}/edit/')
        
    def get_select_url(self, field: models.ForeignKey) -> str:
        """Get the URL for loading select options"""
        related_meta = field.related_model._meta
        return f'/api/{related_meta.app_label}/{related_meta.model_name}/options/'
        
    def get_default_sort_field(self) -> str:
        """Get the default sort field"""
        if self.meta.ordering:
            field_name = self.meta.ordering[0]
            return field_name.lstrip('-')
        return 'id'
        

class ModelConfigRegistry:
    """
    Registry for model configurations
    """
    
    def __init__(self):
        self._configs = {}
        
    def register(self, model: Type[models.Model], config_class: Type[JQGridAutoConfig] = None, **options):
        """Register a model with optional custom configuration"""
        if config_class is None:
            config_class = JQGridAutoConfig
            
        model_key = f'{model._meta.app_label}.{model._meta.model_name}'
        self._configs[model_key] = (model, config_class, options)
        
    def unregister(self, model: Type[models.Model]):
        """Unregister a model"""
        model_key = f'{model._meta.app_label}.{model._meta.model_name}'
        self._configs.pop(model_key, None)
        
    def get_config(self, model: Type[models.Model]) -> JQGridAutoConfig:
        """Get configuration for a model"""
        model_key = f'{model._meta.app_label}.{model._meta.model_name}'
        
        if model_key in self._configs:
            model_class, config_class, options = self._configs[model_key]
            return config_class(model_class, **options)
            
        # Return default configuration if not registered
        return JQGridAutoConfig(model)
    
    def is_registered(self, model: Type[models.Model]) -> bool:
        """Check if a model is registered"""
        model_key = f'{model._meta.app_label}.{model._meta.model_name}'
        return model_key in self._configs
        
    def autodiscover(self, app_names: List[str] = None, exclude_apps: List[str] = None):
        """Auto-discover and register models from apps"""
        if exclude_apps is None:
            exclude_apps = ['django.contrib.admin', 'django.contrib.contenttypes',
                           'django.contrib.sessions', 'django.contrib.auth']
            
        for app_config in apps.get_app_configs():
            if app_names and app_config.name not in app_names:
                continue
            if app_config.name in exclude_apps:
                continue
                
            for model in app_config.get_models():
                if model._meta.managed:
                    self.register(model)
                    

# Global registry instance
jqgrid_registry = ModelConfigRegistry()


def register_model(model: Type[models.Model], **options):
    """Decorator to register a model with custom options"""
    def decorator(config_class: Type[JQGridAutoConfig]):
        jqgrid_registry.register(model, config_class, **options)
        return config_class
    return decorator