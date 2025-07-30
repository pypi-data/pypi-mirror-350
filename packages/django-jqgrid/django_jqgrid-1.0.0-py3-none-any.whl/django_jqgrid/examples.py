"""
Django JQGrid Usage Examples

This file demonstrates how to use the optimized django_jqgrid
with various customization options.
"""
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .optimized_mixin import OptimizedJQGridMixin


# Example 1: Basic Usage
class SimpleGridView(OptimizedJQGridMixin, LoginRequiredMixin, TemplateView):
    """Simple grid with minimal configuration"""
    template_name = 'myapp/grid.html'
    grid_model = 'myapp.Product'  # Can use string or model class
    

# Example 2: Customized Fields
class CustomFieldsGridView(OptimizedJQGridMixin, LoginRequiredMixin, TemplateView):
    """Grid with custom field configuration"""
    template_name = 'myapp/grid.html'
    grid_model = 'myapp.Order'
    
    # Specify which fields to show
    grid_fields = ['order_number', 'customer', 'total', 'status', 'created_at']
    
    # Make some fields read-only
    readonly_fields = ['order_number', 'created_at']
    
    # Hide some fields
    hidden_fields = ['id']
    
    # Custom grid dimensions
    grid_height = 600
    row_num = 50


# Example 3: Custom Formatters and Actions
class AdvancedGridView(OptimizedJQGridMixin, LoginRequiredMixin, TemplateView):
    """Grid with custom formatters and bulk actions"""
    template_name = 'myapp/grid.html'
    grid_model = 'myapp.User'
    
    # Custom formatters
    custom_formatters = {
        'status': '''function(cellvalue, options, rowObject) {
            var colors = {
                'active': 'success',
                'inactive': 'danger',
                'pending': 'warning'
            };
            return '<span class="badge badge-' + colors[cellvalue] + '">' + 
                   cellvalue + '</span>';
        }''',
        'avatar': '''function(cellvalue, options, rowObject) {
            if (cellvalue) {
                return '<img src="' + cellvalue + '" class="avatar-sm">';
            }
            return '<i class="fa fa-user-circle"></i>';
        }'''
    }
    
    # Custom bulk actions
    custom_bulk_actions = [
        {
            'name': 'activate',
            'label': 'Activate Users',
            'icon': 'fa-check',
            'handler': 'activateUsers',
            'confirm': 'Activate selected users?'
        },
        {
            'name': 'send_email',
            'label': 'Send Email',
            'icon': 'fa-envelope',
            'handler': 'sendBulkEmail',
            'modal': True  # Opens in modal
        }
    ]
    
    # Custom buttons
    custom_buttons = {
        'import': {
            'label': 'Import Users',
            'icon': 'fa-upload',
            'handler': 'showImportDialog'
        }
    }


# Example 4: Field-level Customization
class FieldCustomizationView(OptimizedJQGridMixin, LoginRequiredMixin, TemplateView):
    """Grid with field-level customizations"""
    template_name = 'myapp/grid.html'
    grid_model = 'myapp.Product'
    
    def configure_price(self):
        """Custom configuration for price field"""
        return {
            'formatter': 'currency',
            'formatoptions': {
                'prefix': '$',
                'suffix': '',
                'thousandsSeparator': ',',
                'decimalPlaces': 2
            },
            'align': 'right',
            'width': 100
        }
    
    def configure_description(self):
        """Custom configuration for description field"""
        return {
            'edittype': 'textarea',
            'editoptions': {
                'rows': 5,
                'cols': 50
            },
            'search': False,  # Disable search for this field
            'width': 300
        }
    
    def configure_category(self):
        """Custom configuration for category field"""
        return {
            'stype': 'select',
            'searchoptions': {
                'sopt': ['eq', 'ne'],
                'dataUrl': '/api/categories/options/'
            }
        }


# Example 5: Permission-based Grid
class PermissionBasedGridView(OptimizedJQGridMixin, LoginRequiredMixin, TemplateView):
    """Grid with permission-based field visibility"""
    template_name = 'myapp/grid.html'
    grid_model = 'myapp.Employee'
    
    def has_field_permission(self, field_name, action='read'):
        """Check field-level permissions"""
        user = self.request.user
        
        # Only HR can see salary information
        if field_name in ['salary', 'bonus']:
            return user.groups.filter(name='HR').exists()
        
        # Only managers can edit performance ratings
        if field_name == 'performance_rating' and action == 'edit':
            return user.groups.filter(name='Managers').exists()
        
        return True
    
    def can_delete(self):
        """Only admins can bulk delete"""
        return self.request.user.is_superuser
    
    def get_custom_bulk_actions(self):
        """Add role-specific bulk actions"""
        actions = []
        user = self.request.user
        
        if user.groups.filter(name='HR').exists():
            actions.append({
                'name': 'generate_reports',
                'label': 'Generate HR Reports',
                'icon': 'fa-file-pdf',
                'handler': 'generateHRReports'
            })
        
        if user.groups.filter(name='Managers').exists():
            actions.append({
                'name': 'assign_tasks',
                'label': 'Assign Tasks',
                'icon': 'fa-tasks',
                'handler': 'showTaskAssignment'
            })
        
        return actions


# Example 6: Optimized Query Grid
class OptimizedQueryGridView(OptimizedJQGridMixin, LoginRequiredMixin, TemplateView):
    """Grid with query optimization"""
    template_name = 'myapp/grid.html'
    
    def get_model(self):
        """Get model dynamically"""
        from myapp.models import Order
        return Order
    
    def get_optimized_queryset(self, queryset):
        """Add custom query optimizations"""
        # Call parent method for automatic optimization
        queryset = super().get_optimized_queryset(queryset)
        
        # Add custom optimizations
        return queryset.select_related(
            'customer__profile',
            'shipping_address',
            'billing_address'
        ).prefetch_related(
            'items__product',
            'payments'
        ).annotate(
            total_items=models.Count('items'),
            total_paid=models.Sum('payments__amount')
        )


# Example 7: Dynamic Configuration
class DynamicGridView(OptimizedJQGridMixin, LoginRequiredMixin, TemplateView):
    """Grid with dynamic configuration based on request"""
    template_name = 'myapp/grid.html'
    
    def get_model(self):
        """Get model based on URL parameter"""
        model_name = self.kwargs.get('model')
        if model_name == 'products':
            from myapp.models import Product
            return Product
        elif model_name == 'orders':
            from myapp.models import Order
            return Order
        else:
            from myapp.models import Customer
            return Customer
    
    def get_grid_config(self):
        """Customize config based on user preferences"""
        config = super().get_grid_config()
        
        # Apply user's saved preferences
        user_prefs = self.request.session.get('grid_preferences', {})
        if 'row_num' in user_prefs:
            config['options']['rowNum'] = user_prefs['row_num']
        
        if 'hidden_columns' in user_prefs:
            for col in config['colModel']:
                if col['name'] in user_prefs['hidden_columns']:
                    col['hidden'] = True
        
        return config


# Example 8: Using with Django REST Framework ViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

class ProductViewSet(OptimizedJQGridMixin, ModelViewSet):
    """REST API ViewSet with JQGrid configuration"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    @action(detail=False, methods=['GET'])
    def grid_config(self, request):
        """Endpoint to get grid configuration"""
        config = self.get_grid_config()
        return Response(config)
    
    @action(detail=False, methods=['POST'])
    def bulk_action(self, request):
        """Handle bulk actions"""
        action_name = request.data.get('action')
        selected_ids = request.data.get('ids', [])
        
        if action_name == 'activate':
            self.queryset.filter(id__in=selected_ids).update(is_active=True)
            return Response({'status': 'success', 'message': 'Products activated'})
        
        return Response({'status': 'error', 'message': 'Unknown action'})