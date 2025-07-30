from django.contrib import admin
from django import forms
from jsoneditor.forms import JSONEditor

from django_jqgrid.models import GridFilter


class GridFilterForm(forms.ModelForm):
    class Meta:
        model = GridFilter
        fields = '__all__'
        widgets = {
            'value': JSONEditor()
        }

@admin.register(GridFilter)
class GridFilterAdmin(admin.ModelAdmin):
    form = GridFilterForm
    list_display = ('name', 'key', 'table', 'created_by', 'is_global', 'created_at')
    list_filter = ('key', 'is_global', 'table', 'created_by')
    search_fields = ('name', 'value')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'key', 'table', 'created_by', 'is_global')
        }),
        ('Data', {
            'fields': ('value',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
