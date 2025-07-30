"""
Optimized JQGrid Configuration Mixin

This is a DRY, optimized, and highly configurable version of the JqGrid mixin.
"""
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.module_loading import import_string

from .base_mixins import (
    ConfigCacheMixin, QueryOptimizationMixin, 
    FieldConfigurationMixin, BulkActionMixin, PermissionMixin
)
from .conf import jqgrid_settings


class OptimizedJQGridMixin(
    ConfigCacheMixin,
    QueryOptimizationMixin, 
    FieldConfigurationMixin,
    BulkActionMixin,
    PermissionMixin
):
    """
    Optimized mixin for JQGrid configuration.
    
    Features:
    - Configuration caching
    - Query optimization
    - DRY field configuration
    - Highly customizable
    - Hook system for extensions
    """
    
    # Class attributes that can be overridden
    grid_model = None
    grid_fields = None  # List of fields to include
    exclude_fields = []  # List of fields to exclude
    readonly_fields = []  # List of read-only fields
    hidden_fields = []  # List of hidden fields
    
    # Grid options that can be overridden
    grid_height = None
    grid_width = None
    row_num = None
    row_list = None
    
    # Custom configurations
    custom_formatters = {}
    custom_buttons = {}
    custom_bulk_actions = []
    
    def get_model(self):
        """Get the model for this grid"""
        if self.grid_model:
            return self.grid_model
        
        # Try to auto-detect from view
        if hasattr(self, 'model'):
            return self.model
        elif hasattr(self, 'queryset'):
            return self.queryset.model
        
        raise ImproperlyConfigured(
            "OptimizedJQGridMixin requires either a 'grid_model' attribute "
            "or a 'model'/'queryset' attribute on the view."
        )
    
    def get_grid_config(self):
        """Get complete grid configuration"""
        # Check cache first
        cached_config = self.get_cached_config()
        if cached_config:
            return cached_config
        
        # Build configuration
        model = self.get_model()
        config = {
            'model_info': self._get_model_info(model),
            'colModel': self._build_col_model(model),
            'options': self._get_grid_options(),
            'urls': self._get_urls(model),
            'features': self._get_features(),
            'bulk_actions': self.get_bulk_actions(),
            'custom': {
                'formatters': self._get_custom_formatters(),
                'buttons': self._get_custom_buttons(),
            }
        }
        
        # Apply hooks
        config = self._apply_hook('before_config_return', config)
        
        # Cache the configuration
        self.set_cached_config(config)
        
        return config
    
    def _get_model_info(self, model):
        """Get model metadata"""
        meta = model._meta
        return {
            'app_label': meta.app_label,
            'model_name': meta.model_name,
            'verbose_name': str(meta.verbose_name),
            'verbose_name_plural': str(meta.verbose_name_plural),
        }
    
    def _build_col_model(self, model):
        """Build column model configuration"""
        fields = self._get_fields(model)
        col_model = []
        
        # Add action column if needed
        if self._should_include_actions():
            col_model.append(self._get_action_column())
        
        # Add field columns
        for field in fields:
            if self._should_include_field(field):
                col_config = self.build_field_config(field, model)
                col_config = self._apply_field_customizations(field, col_config)
                col_model.append(col_config)
        
        return col_model
    
    def _get_fields(self, model):
        """Get fields to include in grid"""
        if self.grid_fields:
            # Use specified fields
            field_names = self.grid_fields
            fields = []
            for name in field_names:
                try:
                    fields.append(model._meta.get_field(name))
                except models.FieldDoesNotExist:
                    pass
            return fields
        else:
            # Use all fields except excluded
            fields = model._meta.get_fields()
            return [f for f in fields if f.name not in self.exclude_fields]
    
    def _should_include_field(self, field):
        """Check if field should be included"""
        # Skip reverse relations and auto-created fields
        if field.auto_created or field.is_relation and field.many_to_many:
            return False
        
        # Check permissions
        if not self.has_field_permission(field.name):
            return False
        
        return True
    
    def _apply_field_customizations(self, field, config):
        """Apply field-specific customizations"""
        # Apply readonly
        if field.name in self.readonly_fields:
            config['editable'] = False
        
        # Apply hidden
        if field.name in self.hidden_fields:
            config['hidden'] = True
        
        # Apply model-specific config from settings
        model_config = self._get_model_config_from_settings()
        if model_config and 'fields' in model_config:
            field_config = model_config['fields'].get(field.name, {})
            config.update(field_config)
        
        return config
    
    def _get_model_config_from_settings(self):
        """Get model-specific configuration from settings"""
        model = self.get_model()
        model_key = f"{model._meta.app_label}.{model._meta.object_name}"
        return getattr(settings, 'JQGRID_MODEL_CONFIG', {}).get(model_key, {})
    
    def _get_grid_options(self):
        """Get grid options"""
        options = {
            'height': self.grid_height or jqgrid_settings.GRID_HEIGHT,
            'width': self.grid_width or jqgrid_settings.GRID_WIDTH,
            'rowNum': self.row_num or jqgrid_settings.ROW_NUM,
            'rowList': self.row_list or jqgrid_settings.ROW_LIST,
            'pager': True,
            'viewrecords': True,
            'sortorder': 'asc',
            'multiselect': jqgrid_settings.MULTISELECT,
            'multiboxonly': jqgrid_settings.MULTIBOX_ONLY,
            'autowidth': True,
            'shrinkToFit': True,
            'forceFit': True,
            'responsive': True,
            'styleUI': jqgrid_settings.GUI_STYLE,
            'iconSet': jqgrid_settings.ICON_SET,
        }
        
        # Apply model-specific options
        model_config = self._get_model_config_from_settings()
        if model_config and 'options' in model_config:
            options.update(model_config['options'])
        
        return options
    
    def _get_urls(self, model):
        """Get URLs for grid operations"""
        meta = model._meta
        base_url = f"/api/{meta.app_label}/{meta.model_name}/"
        
        return {
            'list': base_url,
            'create': f"{base_url}create/",
            'edit': f"{base_url}edit/",
            'delete': f"{base_url}delete/",
            'bulk': f"{base_url}bulk/",
            'export': f"{base_url}export/",
            'import': f"{base_url}import/",
        }
    
    def _get_features(self):
        """Get enabled features"""
        return {
            'import_export': jqgrid_settings.ENABLE_IMPORT_EXPORT,
            'filters': jqgrid_settings.ENABLE_FILTERS,
            'column_chooser': jqgrid_settings.ENABLE_COLUMN_CHOOSER,
            'freeze_columns': jqgrid_settings.ENABLE_FREEZE_COLUMNS,
            'search': True,
            'refresh': True,
            'fullscreen': True,
        }
    
    def _should_include_actions(self):
        """Check if actions column should be included"""
        return True  # Can be overridden
    
    def _get_action_column(self):
        """Get configuration for actions column"""
        return {
            'name': 'actions',
            'index': 'actions',
            'label': 'Actions',
            'width': 80,
            'fixed': True,
            'sortable': False,
            'search': False,
            'formatter': 'actions',
            'formatoptions': {
                'keys': True,
                'editformbutton': True,
                'delbutton': True,
            }
        }
    
    def _get_custom_formatters(self):
        """Get custom formatters"""
        formatters = {}
        
        # Add class-level formatters
        formatters.update(self.custom_formatters)
        
        # Add formatters from settings
        settings_formatters = jqgrid_settings.CUSTOM_FORMATTERS or {}
        formatters.update(settings_formatters)
        
        return formatters
    
    def _get_custom_buttons(self):
        """Get custom buttons"""
        buttons = {}
        
        # Add class-level buttons
        buttons.update(self.custom_buttons)
        
        # Add buttons from model config
        model_config = self._get_model_config_from_settings()
        if model_config and 'buttons' in model_config:
            buttons.update(model_config['buttons'])
        
        return buttons
    
    def get_custom_bulk_actions(self):
        """Get custom bulk actions"""
        actions = list(self.custom_bulk_actions)
        
        # Add actions from model config
        model_config = self._get_model_config_from_settings()
        if model_config and 'bulk_actions' in model_config:
            actions.extend(model_config['bulk_actions'])
        
        return actions
    
    def _apply_hook(self, hook_name, data):
        """Apply a hook if configured"""
        hooks = getattr(jqgrid_settings, 'HOOKS', {})
        hook_path = hooks.get(hook_name)
        
        if hook_path:
            try:
                hook_func = import_string(hook_path)
                return hook_func(self, data)
            except (ImportError, AttributeError):
                pass
        
        return data