from django.core.management.base import BaseCommand
from django.apps import apps
from django_jqgrid.auto_config import jqgrid_registry


class Command(BaseCommand):
    help = 'Discover and auto-configure Django models for jqGrid'

    def add_arguments(self, parser):
        parser.add_argument(
            '--app',
            type=str,
            help='Specific app to discover models from',
        )
        parser.add_argument(
            '--list',
            action='store_true',
            help='List all registered models',
        )

    def handle(self, *args, **options):
        if options['list']:
            self.list_registered_models()
            return

        app_label = options.get('app')
        
        if app_label:
            # Discover models from specific app
            try:
                app_config = apps.get_app_config(app_label)
                models = app_config.get_models()
                self.stdout.write(f"Discovering models from {app_label}...")
                
                for model in models:
                    if not jqgrid_registry.is_registered(model):
                        jqgrid_registry.register(model)
                        self.stdout.write(
                            self.style.SUCCESS(f"   Registered {model._meta.label}")
                        )
                    else:
                        self.stdout.write(
                            f"  - {model._meta.label} already registered"
                        )
            except LookupError:
                self.stdout.write(
                    self.style.ERROR(f"App '{app_label}' not found")
                )
        else:
            # Discover models from all apps
            self.stdout.write("Discovering models from all apps...")
            
            for app_config in apps.get_app_configs():
                # Skip Django's built-in apps by default
                if app_config.name.startswith('django.'):
                    continue
                    
                models = app_config.get_models()
                if models:
                    self.stdout.write(f"\n{app_config.verbose_name}:")
                    
                    for model in models:
                        if not jqgrid_registry.is_registered(model):
                            jqgrid_registry.register(model)
                            self.stdout.write(
                                self.style.SUCCESS(f"   Registered {model._meta.label}")
                            )
                        else:
                            self.stdout.write(
                                f"  - {model._meta.label} already registered"
                            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nTotal models registered: {len(jqgrid_registry._configs)}"
            )
        )

    def list_registered_models(self):
        """List all currently registered models"""
        registered_models = jqgrid_registry._configs
        
        if not registered_models:
            self.stdout.write("No models currently registered.")
            return
            
        self.stdout.write("Currently registered models:")
        for model_key, (model_class, config_class, options) in registered_models.items():
            self.stdout.write(f"  - {model_class._meta.label}")