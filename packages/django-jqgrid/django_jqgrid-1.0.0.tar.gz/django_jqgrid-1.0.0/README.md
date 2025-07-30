# Django JQGrid

[![PyPI version](https://badge.fury.io/py/django-jqgrid.svg)](https://badge.fury.io/py/django-jqgrid)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-jqgrid.svg)](https://pypi.org/project/django-jqgrid/)
[![Django Versions](https://img.shields.io/pypi/djversions/django-jqgrid.svg)](https://pypi.org/project/django-jqgrid/)
[![License](https://img.shields.io/pypi/l/django-jqgrid.svg)](https://github.com/coder-aniket/django-jqgrid/blob/master/LICENSE)

A Django package for easy integration of jqGrid with automatic configuration, comprehensive CRUD operations, and advanced features. This package makes it trivial to add powerful, interactive data grids to your Django applications with minimal code.

## Features

- ⚙️ **Auto-configuration** - Automatically discovers and configures Django models
- 🚀 **Full CRUD Support** - Create, Read, Update, Delete operations out of the box
- 🔍 **Advanced Filtering** - Built-in search and filtering capabilities
- 📊 **Import/Export** - Excel and CSV import/export functionality
- 🎨 **Highly Customizable** - Extensive configuration options
- ⚡ **Performance Optimized** - Query optimization and caching support
- 🔒 **Security** - CSRF protection and field-level permissions
- 🗄️ **Multi-database** - Support for multiple databases
- 📱 **Responsive** - Mobile-friendly grid layouts
- 🔧 **DRY Principle** - Reusable components and mixins

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Basic Usage](#basic-usage)
- [Advanced Usage](#advanced-usage)
- [Customization](#customization)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Using pip

```bash
pip install django-jqgrid
```

### Using poetry

```bash
poetry add django-jqgrid
```

### Development Installation

```bash
git clone https://github.com/coder-aniket/django-jqgrid.git
cd django-jqgrid
pip install -e .
```

## Quick Start

1. Add `django_jqgrid` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    'django_jqgrid',
    ...
]
```

2. Include the URLconf in your project:

```python
# urls.py
from django.urls import path, include

urlpatterns = [
    ...
    path('jqgrid/', include('django_jqgrid.urls')),
    ...
]
```

3. Run the auto-discovery command:

```bash
python manage.py discover_models
```

4. Add the grid to your template:

```html
{% load jqgrid_tags %}

<!DOCTYPE html>
<html>
<head>
    {% jqgrid_css %}
</head>
<body>
    {% jqgrid_render 'MyModel' %}
    
    {% jqgrid_js %}
</body>
</html>
```

That's it! You now have a fully functional data grid with CRUD operations.

## Configuration

### Settings

Add to your `settings.py`:

```python
JQGRID_CONFIG = {
    'DEFAULT_ROWS_PER_PAGE': 20,
    'ENABLE_EXCEL_EXPORT': True,
    'ENABLE_CSV_EXPORT': True,
    'ENABLE_FILTERING': True,
    'ENABLE_CRUD_OPERATIONS': True,
    'DATE_FORMAT': '%Y-%m-%d',
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DECIMAL_PLACES': 2,
    'THOUSAND_SEPARATOR': ',',
    'CACHE_TIMEOUT': 300,  # seconds
    'USE_CACHE': True,
}
```

### Model Configuration

```python
from django.db import models
from django_jqgrid.mixins import JQGridMixin

class Product(JQGridMixin, models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class JQGridMeta:
        # Grid configuration
        grid_config = {
            'caption': 'Product Management',
            'height': 'auto',
            'autowidth': True,
            'rownumbers': True,
            'sortname': 'name',
            'sortorder': 'asc',
        }
        
        # Column configuration
        column_config = {
            'name': {
                'label': 'Product Name',
                'width': 200,
                'searchable': True,
                'editable': True,
            },
            'price': {
                'label': 'Price',
                'width': 100,
                'formatter': 'currency',
                'align': 'right',
            },
            'stock': {
                'label': 'Stock Quantity',
                'width': 120,
                'formatter': 'integer',
                'align': 'center',
            },
        }
        
        # Fields to exclude from grid
        exclude_fields = ['id', 'created_at']
        
        # Enable features
        enable_excel_export = True
        enable_csv_export = True
        enable_crud = True
        enable_search = True
```

## Basic Usage

### Simple Grid

```python
# views.py
from django.shortcuts import render
from django_jqgrid.views import JQGridView
from .models import Product

class ProductGridView(JQGridView):
    model = Product
    template_name = 'products/grid.html'
```

### Template

```html
<!-- products/grid.html -->
{% extends "base.html" %}
{% load jqgrid_tags %}

{% block content %}
    <h1>Products</h1>
    {% jqgrid_render model="Product" %}
{% endblock %}

{% block extra_js %}
    {% jqgrid_js %}
{% endblock %}
```

### URL Configuration

```python
# urls.py
from django.urls import path
from .views import ProductGridView

urlpatterns = [
    path('products/', ProductGridView.as_view(), name='product-grid'),
]
```

## Advanced Usage

### Custom Actions

```python
from django_jqgrid.views import JQGridView
from django.http import JsonResponse

class ProductGridView(JQGridView):
    model = Product
    
    def custom_action(self, request, pk):
        """Custom action for grid rows"""
        product = self.get_object(pk)
        # Your custom logic here
        return JsonResponse({'success': True})
    
    def get_grid_config(self):
        config = super().get_grid_config()
        config.update({
            'custom_actions': [
                {
                    'name': 'custom_action',
                    'label': 'Custom Action',
                    'icon': 'fa-star',
                    'callback': 'customActionCallback'
                }
            ]
        })
        return config
```

### Custom Filters

```python
from django_jqgrid.filters import JQGridFilter

class PriceRangeFilter(JQGridFilter):
    def filter_queryset(self, queryset, value):
        if '-' in value:
            min_price, max_price = value.split('-')
            return queryset.filter(
                price__gte=min_price,
                price__lte=max_price
            )
        return queryset

class ProductGridView(JQGridView):
    model = Product
    custom_filters = {
        'price_range': PriceRangeFilter()
    }
```

### Bulk Operations

```python
class ProductGridView(JQGridView):
    model = Product
    enable_bulk_operations = True
    
    def bulk_update_stock(self, request, selected_ids):
        """Bulk update stock for selected products"""
        new_stock = request.POST.get('new_stock')
        Product.objects.filter(id__in=selected_ids).update(stock=new_stock)
        return JsonResponse({'success': True, 'updated': len(selected_ids)})
    
    def get_bulk_actions(self):
        return [
            {
                'name': 'bulk_update_stock',
                'label': 'Update Stock',
                'icon': 'fa-boxes',
                'form_fields': [
                    {'name': 'new_stock', 'type': 'number', 'label': 'New Stock'}
                ]
            }
        ]
```

### Dynamic Column Configuration

```python
class ProductGridView(JQGridView):
    model = Product
    
    def get_column_config(self):
        config = super().get_column_config()
        
        # Dynamic column visibility based on user permissions
        if not self.request.user.has_perm('products.view_price'):
            config['price']['hidden'] = True
            
        # Add computed columns
        config['total_value'] = {
            'label': 'Total Value',
            'formatter': 'currency',
            'computed': True,
            'formula': 'price * stock'
        }
        
        return config
```

## Customization

### Custom Templates

Create custom templates for different parts of the grid:

```html
<!-- templates/jqgrid/custom_grid.html -->
{% extends "django_jqgrid/grid_base.html" %}

{% block grid_toolbar %}
    <div class="custom-toolbar">
        <button id="custom-button">Custom Action</button>
    </div>
    {{ block.super }}
{% endblock %}

{% block grid_footer %}
    <div class="custom-footer">
        Custom footer content
    </div>
{% endblock %}
```

### JavaScript Callbacks

```javascript
// static/js/grid_callbacks.js
function customActionCallback(rowId) {
    $.ajax({
        url: '/products/custom-action/' + rowId + '/',
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function(response) {
            $('#grid').trigger('reloadGrid');
            showNotification('Action completed successfully');
        }
    });
}

// Grid event handlers
$(document).on('jqGrid:afterLoad', function(e, gridId) {
    console.log('Grid loaded:', gridId);
});

$(document).on('jqGrid:beforeSave', function(e, rowData) {
    // Validate before saving
    if (rowData.price < 0) {
        e.preventDefault();
        alert('Price cannot be negative');
    }
});
```

### CSS Customization

```css
/* static/css/custom_grid.css */
.ui-jqgrid {
    font-family: 'Roboto', sans-serif;
}

.ui-jqgrid-htable th {
    background-color: #2c3e50;
    color: white;
}

.ui-jqgrid-bdiv tr:hover {
    background-color: #ecf0f1;
}

/* Custom cell styling */
.grid-cell-warning {
    background-color: #f39c12 !important;
    color: white;
}

.grid-cell-danger {
    background-color: #e74c3c !important;
    color: white;
}
```

## API Reference

### View Classes

#### JQGridView

Base view for rendering jqGrid.

**Attributes:**
- `model` - Django model class
- `template_name` - Template to render
- `paginate_by` - Number of rows per page
- `enable_export` - Enable/disable export functionality
- `enable_crud` - Enable/disable CRUD operations

**Methods:**
- `get_queryset()` - Returns the base queryset
- `get_grid_config()` - Returns grid configuration
- `get_column_config()` - Returns column configuration
- `process_grid_request()` - Handles AJAX grid requests

#### JQGridAPIView

REST API view for grid data.

**Methods:**
- `list()` - GET method for retrieving grid data
- `create()` - POST method for creating records
- `update()` - PUT method for updating records
- `destroy()` - DELETE method for deleting records

### Template Tags

#### jqgrid_render

Renders the complete grid.

```django
{% jqgrid_render model="ModelName" config=grid_config %}
```

**Parameters:**
- `model` - Model name or instance
- `config` - Optional configuration dictionary
- `height` - Grid height (default: 'auto')
- `width` - Grid width (default: 'auto')

#### jqgrid_css

Includes required CSS files.

```django
{% jqgrid_css theme="bootstrap4" %}
```

#### jqgrid_js

Includes required JavaScript files.

```django
{% jqgrid_js include_locale=True %}
```

### Mixins

#### JQGridMixin

Model mixin that adds jqGrid functionality.

**Class Attributes:**
- `JQGridMeta` - Configuration class

**Methods:**
- `get_grid_data()` - Returns formatted data for grid
- `get_display_value()` - Returns display value for field

#### JQGridQuerysetMixin

Mixin for queryset optimization.

**Methods:**
- `optimized_for_grid()` - Returns optimized queryset
- `with_annotations()` - Adds grid-specific annotations

## Examples

### Complete Working Example

```python
# models.py
from django.db import models
from django_jqgrid.mixins import JQGridMixin

class Order(JQGridMixin, models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class JQGridMeta:
        grid_config = {
            'caption': 'Order Management',
            'multiselect': True,
            'multiboxonly': True,
        }
        
        column_config = {
            'order_number': {
                'label': 'Order #',
                'width': 120,
                'frozen': True,
            },
            'customer_name': {
                'label': 'Customer',
                'width': 200,
            },
            'status': {
                'label': 'Status',
                'width': 100,
                'formatter': 'select',
                'stype': 'select',
                'searchoptions': {
                    'value': ':All;pending:Pending;processing:Processing;shipped:Shipped;delivered:Delivered'
                }
            },
            'total_amount': {
                'label': 'Total',
                'width': 100,
                'formatter': 'currency',
                'align': 'right',
            }
        }

# views.py
from django_jqgrid.views import JQGridView
from django.db.models import Q

class OrderGridView(JQGridView):
    model = Order
    template_name = 'orders/list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Add custom filtering
        if self.request.GET.get('status'):
            queryset = queryset.filter(status=self.request.GET['status'])
        return queryset.select_related('product')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Order._meta.get_field('status').choices
        return context

# templates/orders/list.html
{% extends "base.html" %}
{% load jqgrid_tags %}

{% block content %}
<div class="container-fluid">
    <h1>Orders</h1>
    
    <!-- Status Filter -->
    <div class="mb-3">
        <select id="status-filter" class="form-control">
            <option value="">All Status</option>
            {% for value, label in status_choices %}
                <option value="{{ value }}">{{ label }}</option>
            {% endfor %}
        </select>
    </div>
    
    <!-- Grid -->
    {% jqgrid_render model="Order" %}
    
    <!-- Custom Buttons -->
    <div class="mt-3">
        <button id="export-selected" class="btn btn-primary">Export Selected</button>
        <button id="bulk-update-status" class="btn btn-warning">Update Status</button>
    </div>
</div>
{% endblock %}

{% block extra_js %}
{% jqgrid_js %}
<script>
$(document).ready(function() {
    // Status filter
    $('#status-filter').on('change', function() {
        var status = $(this).val();
        $('#grid').jqGrid('setGridParam', {
            postData: { status: status }
        }).trigger('reloadGrid');
    });
    
    // Export selected rows
    $('#export-selected').on('click', function() {
        var selectedRows = $('#grid').jqGrid('getGridParam', 'selarrrow');
        if (selectedRows.length === 0) {
            alert('Please select rows to export');
            return;
        }
        
        window.location.href = '/orders/export/?ids=' + selectedRows.join(',');
    });
    
    // Bulk update status
    $('#bulk-update-status').on('click', function() {
        var selectedRows = $('#grid').jqGrid('getGridParam', 'selarrrow');
        if (selectedRows.length === 0) {
            alert('Please select rows to update');
            return;
        }
        
        var newStatus = prompt('Enter new status (pending/processing/shipped/delivered):');
        if (newStatus) {
            $.ajax({
                url: '/orders/bulk-update-status/',
                method: 'POST',
                data: {
                    ids: selectedRows,
                    status: newStatus,
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                },
                success: function(response) {
                    $('#grid').trigger('reloadGrid');
                    alert('Updated ' + response.updated + ' orders');
                }
            });
        }
    });
});
</script>
{% endblock %}
```

### Multi-Database Example

```python
# views.py
from django_jqgrid.views import JQGridView

class MultiDBGridView(JQGridView):
    model = Product
    using = 'warehouse_db'  # Specify database
    
    def get_queryset(self):
        # Use specific database
        return self.model.objects.using(self.using).all()

# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'main_db',
        # ... other settings
    },
    'warehouse_db': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'warehouse',
        # ... other settings
    }
}
```

### Custom Cell Rendering

```python
# models.py
class Product(JQGridMixin, models.Model):
    name = models.CharField(max_length=100)
    stock = models.IntegerField()
    
    class JQGridMeta:
        column_config = {
            'stock': {
                'label': 'Stock',
                'width': 100,
                'cellattr': 'stockCellAttr',
                'formatter': 'stockFormatter'
            }
        }

# In your template
{% block extra_js %}
<script>
function stockFormatter(cellvalue, options, rowObject) {
    if (cellvalue < 10) {
        return '<span class="text-danger font-weight-bold">' + cellvalue + '</span>';
    } else if (cellvalue < 50) {
        return '<span class="text-warning">' + cellvalue + '</span>';
    }
    return '<span class="text-success">' + cellvalue + '</span>';
}

function stockCellAttr(rowId, val, rawObject, cm, rdata) {
    if (parseInt(val) < 10) {
        return 'class="bg-danger text-white"';
    }
    return '';
}
</script>
{% endblock %}
```

## Performance Optimization

### Query Optimization

```python
from django_jqgrid.mixins import JQGridOptimizedMixin

class OptimizedProductView(JQGridOptimizedMixin, JQGridView):
    model = Product
    
    # Specify related fields to prefetch
    prefetch_related = ['category', 'tags']
    select_related = ['manufacturer']
    
    # Only load necessary fields
    only_fields = ['id', 'name', 'price', 'stock', 'category__name']
    
    # Add database indexes
    class Meta:
        indexes = [
            models.Index(fields=['name', 'price']),
            models.Index(fields=['stock']),
        ]
```

### Caching

```python
from django.core.cache import cache
from django_jqgrid.views import JQGridView

class CachedGridView(JQGridView):
    model = Product
    cache_timeout = 300  # 5 minutes
    
    def get_grid_data(self, request):
        cache_key = f'grid_data_{self.model.__name__}_{request.GET.urlencode()}'
        data = cache.get(cache_key)
        
        if data is None:
            data = super().get_grid_data(request)
            cache.set(cache_key, data, self.cache_timeout)
            
        return data
```

## Security

### Field-Level Permissions

```python
class SecureGridView(JQGridView):
    model = Product
    
    def get_column_config(self):
        config = super().get_column_config()
        user = self.request.user
        
        # Hide sensitive fields based on permissions
        if not user.has_perm('products.view_cost'):
            config['cost']['hidden'] = True
            
        # Make fields read-only based on permissions
        if not user.has_perm('products.change_price'):
            config['price']['editable'] = False
            
        return config
    
    def check_crud_permission(self, action):
        """Check if user has permission for CRUD action"""
        permission_map = {
            'create': 'products.add_product',
            'update': 'products.change_product',
            'delete': 'products.delete_product',
        }
        
        return self.request.user.has_perm(permission_map.get(action, ''))
```

### CSRF Protection

All AJAX requests include CSRF protection by default. Custom implementations:

```javascript
// Ensure CSRF token is included in all AJAX requests
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type)) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
```

## Troubleshooting

### Common Issues

1. **Grid not loading data**
   - Check browser console for JavaScript errors
   - Verify URLs are correctly configured
   - Check Django debug toolbar for query issues

2. **Export not working**
   - Ensure `django_jqgrid` is in INSTALLED_APPS
   - Check that `MEDIA_ROOT` is configured
   - Verify user has export permissions

3. **Editing not saving**
   - Check CSRF token is included
   - Verify model has proper permissions
   - Check for validation errors in response

### Debug Mode

Enable debug mode for detailed logging:

```python
# settings.py
JQGRID_CONFIG = {
    'DEBUG': True,
    'LOG_LEVEL': 'DEBUG',
}

# views.py
import logging

logger = logging.getLogger('django_jqgrid')

class DebugGridView(JQGridView):
    model = Product
    
    def get_grid_data(self, request):
        logger.debug(f"Grid request: {request.GET}")
        data = super().get_grid_data(request)
        logger.debug(f"Returning {len(data['rows'])} rows")
        return data
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/coder-aniket/django-jqgrid.git
cd django-jqgrid

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
flake8
black .
isort .
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=django_jqgrid

# Run specific test file
pytest tests/test_views.py

# Run with verbose output
pytest -v
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on top of the excellent [jqGrid](https://github.com/tonytomov/jqGrid) library
- Inspired by Django's admin interface
- Thanks to all our contributors

## Support

- 📧 Email: coder.aniketp@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/coder-aniket/django-jqgrid/issues)
- 📖 Documentation: [Read the Docs](https://django-jqgrid.readthedocs.io)
- 💬 Discussions: [GitHub Discussions](https://github.com/coder-aniket/django-jqgrid/discussions)

---

Made with ❤️ by the Django JQGrid team