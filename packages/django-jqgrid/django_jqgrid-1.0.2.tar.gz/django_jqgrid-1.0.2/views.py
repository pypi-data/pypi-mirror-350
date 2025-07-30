from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.views.generic import TemplateView
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django_jqgrid.models import GridFilter
from django_jqgrid.serializers import GridFilterSerializer
from django_jqgrid.mixins import JqGridConfigMixin


class GridFilterViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing grid filters
    """
    queryset = GridFilter.objects.all()
    serializer_class = GridFilterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all filters for the currently authenticated user
        and any global filters.
        """
        user = self.request.user
        # Return both user-specific and global filters
        return GridFilter.objects.filter(
            # Filter for the current user's filters OR global filters
            models.Q(created_by=user) | models.Q(is_global=True)
        ).order_by('-created_at')

    @action(detail=False, methods=['get'])
    def by_table(self, request):
        """
        Return filters for a specific table (content type)
        """
        app_name = request.query_params.get('app_name')
        model_name = request.query_params.get('model')

        if not app_name or not model_name:
            return Response(
                {"error": "Both app_name and model parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get content type for this app/model
            content_type = ContentType.objects.get(app_label=app_name, model=model_name)

            # Get filters for this content type
            filters = self.get_queryset().filter(table=content_type)
            serializer = self.get_serializer(filters, many=True)

            return Response({
                "status": "success",
                "data": {
                    "content_type": {
                        "id": content_type.id,
                        "app_label": content_type.app_label,
                        "model": content_type.model
                    },
                    "filters": serializer.data
                }
            })
        except ContentType.DoesNotExist:
            return Response(
                {"error": f"Content type for {app_name}.{model_name} not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class JQGridView(JqGridConfigMixin, TemplateView):
    """
    Generic view for displaying jqGrid tables
    """
    template_name = 'django_jqgrid/grid_container.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add jqGrid specific context if needed
        context['grid_config'] = self.get_grid_config()
        return context
