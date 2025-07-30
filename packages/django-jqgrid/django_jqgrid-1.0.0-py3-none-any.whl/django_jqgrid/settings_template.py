"""
Django JQGrid Settings Template

Copy this to your Django settings file and customize as needed.
All settings are optional - defaults will be used if not specified.
"""

JQGRID_CONFIG = {
    # Grid Display Settings
    'GRID_HEIGHT': 400,  # Height in pixels or 'auto'
    'GRID_WIDTH': 'auto',  # Width in pixels or 'auto'
    'ROW_NUM': 25,  # Default rows per page
    'ROW_LIST': [10, 25, 50, 100, 500, 1000],  # Page size options
    'MULTISELECT': True,  # Enable row selection
    'MULTIBOX_ONLY': True,  # Select only via checkbox
    
    # UI Settings
    'ICON_SET': 'fontAwesome',  # Icon set: 'fontAwesome', 'glyph', 'ui'
    'GUI_STYLE': 'bootstrap4',  # Style: 'bootstrap4', 'bootstrap5', 'jqueryui'
    'LOCALE': 'en',  # Language locale
    
    # Form Settings
    'FORM_COLUMNS': 4,  # Number of columns in edit form
    'FORM_WIDTH': 800,  # Form width in pixels
    'FORM_HEIGHT': 'auto',  # Form height
    
    # Date/Time Formats
    'DATE_FORMAT': 'Y-m-d',
    'DATETIME_FORMAT': 'Y-m-d H:i:s',
    'TIME_FORMAT': 'H:i:s',
    
    # Search Operators by Field Type
    'SEARCH_OPERATORS': {
        'text': ['eq', 'ne', 'cn', 'nc', 'bw', 'bn', 'ew', 'en'],
        'number': ['eq', 'ne', 'lt', 'le', 'gt', 'ge'],
        'date': ['eq', 'ne', 'lt', 'le', 'gt', 'ge'],
        'boolean': ['eq', 'ne'],
        'select': ['eq', 'ne', 'in', 'ni'],
    },
    
    # Field Type Mappings
    'FIELD_TYPE_MAP': {
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
        # Add custom field types here
    },
    
    # Performance Settings
    'ENABLE_CACHE': True,  # Cache grid configurations
    'CACHE_TIMEOUT': 300,  # Cache timeout in seconds
    'OPTIMIZE_QUERIES': True,  # Use select_related/prefetch_related
    'DEFAULT_PAGE_SIZE': 50,  # Default page size
    'MAX_PAGE_SIZE': 1000,  # Maximum allowed page size
    
    # Security Settings
    'ENABLE_CSRF': True,  # Enable CSRF protection
    'FIELD_LEVEL_PERMISSIONS': False,  # Enable field-level permissions
    'AUDIT_CHANGES': False,  # Log all changes
    
    # Plugin Settings
    'ENABLE_IMPORT_EXPORT': True,  # Enable import/export functionality
    'ENABLE_FILTERS': True,  # Enable advanced filters
    'ENABLE_COLUMN_CHOOSER': True,  # Enable column chooser
    'ENABLE_FREEZE_COLUMNS': False,  # Enable column freezing
    
    # Static Files Configuration
    'STATIC_URL_PREFIX': '/static/django_jqgrid/',
    'USE_CDN': False,  # Use CDN for jqGrid files
    'CDN_BASE_URL': 'https://cdn.jsdelivr.net/npm/',
    
    # Custom Formatters (JavaScript functions as strings)
    'CUSTOM_FORMATTERS': {
        'status': '''function(cellvalue, options, rowObject) {
            var colors = {'active': 'success', 'inactive': 'danger'};
            return '<span class="badge badge-' + colors[cellvalue] + '">' + cellvalue + '</span>';
        }''',
    },
    
    # Custom CSS Classes
    'CUSTOM_CSS_CLASSES': {
        'grid_container': 'jqgrid-container',
        'grid_table': 'table table-striped',
        'pager': 'jqgrid-pager',
    },
    
    # Hooks for customization
    'HOOKS': {
        'before_grid_init': 'myapp.jqgrid_hooks.before_grid_init',
        'after_grid_init': 'myapp.jqgrid_hooks.after_grid_init',
        'before_save': 'myapp.jqgrid_hooks.before_save',
        'after_save': 'myapp.jqgrid_hooks.after_save',
    },
}

# Example of custom field configurations per model
JQGRID_MODEL_CONFIG = {
    'myapp.MyModel': {
        'fields': {
            'status': {
                'formatter': 'status',  # Use custom formatter defined above
                'width': 100,
                'align': 'center',
            },
            'created_at': {
                'hidden': True,  # Hide this field
            },
            'description': {
                'edittype': 'textarea',
                'editoptions': {'rows': 5, 'cols': 40},
            },
        },
        'options': {
            'height': 600,  # Override default height for this model
            'rowNum': 50,  # Different default page size
        },
        'bulk_actions': [
            {
                'name': 'approve',
                'label': 'Approve Selected',
                'icon': 'fa-check',
                'handler': 'myapp.bulk_actions.approve_items',
                'confirm': 'Approve selected items?',
            },
        ],
    },
}