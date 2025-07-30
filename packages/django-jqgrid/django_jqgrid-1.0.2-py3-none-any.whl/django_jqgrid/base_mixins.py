"""
Optimized base mixins for django_jqgrid that follow DRY principles
"""
from functools import lru_cache
from django.core.cache import cache
from django.db.models import Prefetch, Q
from django.contrib.contenttypes.models import ContentType

from .conf import jqgrid_settings, get_field_config, get_search_operators


class ConfigCacheMixin:
    """Mixin to provide configuration caching"""
    
    @property
    def cache_key(self):
        """Generate cache key for this configuration"""
        model_meta = self.get_model()._meta
        return f"jqgrid:config:{model_meta.app_label}:{model_meta.model_name}"
    
    def get_cached_config(self):
        """Get configuration from cache if available"""
        if not jqgrid_settings.ENABLE_CACHE:
            return None
        return cache.get(self.cache_key)
    
    def set_cached_config(self, config):
        """Cache configuration"""
        if jqgrid_settings.ENABLE_CACHE:
            cache.set(self.cache_key, config, jqgrid_settings.CACHE_TIMEOUT)
    
    def clear_cache(self):
        """Clear cached configuration"""
        cache.delete(self.cache_key)


class QueryOptimizationMixin:
    """Mixin to optimize database queries"""
    
    def get_optimized_queryset(self, queryset):
        """Apply query optimizations"""
        if not jqgrid_settings.OPTIMIZE_QUERIES:
            return queryset
            
        model = queryset.model
        meta = model._meta
        
        # Collect foreign keys and many-to-many fields
        fk_fields = []
        m2m_fields = []
        
        for field in meta.get_fields():
            if field.many_to_one or field.one_to_one:
                fk_fields.append(field.name)
            elif field.many_to_many and not field.auto_created:
                m2m_fields.append(field.name)
        
        # Apply select_related for foreign keys
        if fk_fields:
            queryset = queryset.select_related(*fk_fields)
        
        # Apply prefetch_related for many-to-many
        if m2m_fields:
            queryset = queryset.prefetch_related(*m2m_fields)
        
        return queryset
    
    def get_field_lookups(self, model):
        """Get field lookups for optimization"""
        lookups = {
            'select_related': [],
            'prefetch_related': [],
        }
        
        for field in model._meta.get_fields():
            if field.many_to_one or field.one_to_one:
                lookups['select_related'].append(field.name)
            elif field.many_to_many and not field.auto_created:
                lookups['prefetch_related'].append(field.name)
        
        return lookups


class FieldConfigurationMixin:
    """Mixin to handle field configuration in a DRY way"""
    
    @lru_cache(maxsize=None)
    def get_field_type_config(self, field_class_name):
        """Get configuration for a field type with caching"""
        return get_field_config(field_class_name)
    
    def build_field_config(self, field, model):
        """Build configuration for a single field"""
        field_class_name = field.__class__.__name__
        base_config = self.get_field_type_config(field_class_name)
        
        # Common attributes
        config = {
            'name': field.name,
            'index': field.name,
            'label': field.verbose_name.title(),
            'editable': not field.primary_key and field.editable,
            'hidden': field.name.endswith('_ptr') or field.name == 'id',
            'search': True,
            'sortable': True,
        }
        
        # Merge with base config
        config.update(base_config)
        
        # Field-specific adjustments
        if hasattr(field, 'max_length') and field.max_length:
            config['editrules']['maxlength'] = field.max_length
            # Calculate width based on max_length
            config['width'] = min(150, field.max_length * 7)
        
        if not field.blank:
            config['editrules']['required'] = True
        
        if hasattr(field, 'choices') and field.choices:
            config['edittype'] = 'select'
            config['formatter'] = 'select'
            choices_dict = ':'.join([f"{k}:{v}" for k, v in field.choices])
            config['editoptions'] = {'value': choices_dict}
            config['searchoptions']['value'] = choices_dict
        
        # Apply user customizations
        custom_config = self.get_custom_field_config(field.name)
        if custom_config:
            config.update(custom_config)
        
        return config
    
    def get_custom_field_config(self, field_name):
        """Hook for user to provide custom field configuration"""
        # This can be overridden in subclasses
        return getattr(self, f'configure_{field_name}', lambda: {})()


class BulkActionMixin:
    """Mixin to handle bulk actions in a configurable way"""
    
    def get_bulk_actions(self):
        """Get configured bulk actions"""
        default_actions = []
        
        if self.can_delete():
            default_actions.append({
                'name': 'delete',
                'label': 'Delete Selected',
                'icon': 'fa-trash',
                'confirm': 'Are you sure you want to delete the selected items?',
                'handler': 'defaultBulkDelete',
            })
        
        if self.can_export():
            default_actions.extend([
                {
                    'name': 'export_excel',
                    'label': 'Export to Excel',
                    'icon': 'fa-file-excel',
                    'handler': 'defaultBulkExport',
                    'params': {'format': 'xlsx'}
                },
                {
                    'name': 'export_csv',
                    'label': 'Export to CSV',
                    'icon': 'fa-file-csv',
                    'handler': 'defaultBulkExport',
                    'params': {'format': 'csv'}
                }
            ])
        
        # Add custom actions
        custom_actions = self.get_custom_bulk_actions()
        return default_actions + custom_actions
    
    def get_custom_bulk_actions(self):
        """Hook for custom bulk actions"""
        return []
    
    def can_delete(self):
        """Check if user can perform bulk delete"""
        return True
    
    def can_export(self):
        """Check if user can export data"""
        return jqgrid_settings.ENABLE_IMPORT_EXPORT


class PermissionMixin:
    """Mixin to handle permissions"""
    
    def has_field_permission(self, field_name, action='read'):
        """Check field-level permission"""
        if not jqgrid_settings.FIELD_LEVEL_PERMISSIONS:
            return True
        
        # Override in subclass for custom logic
        return True
    
    def filter_fields_by_permission(self, fields):
        """Filter fields based on permissions"""
        if not jqgrid_settings.FIELD_LEVEL_PERMISSIONS:
            return fields
        
        return [
            field for field in fields 
            if self.has_field_permission(field.name)
        ]