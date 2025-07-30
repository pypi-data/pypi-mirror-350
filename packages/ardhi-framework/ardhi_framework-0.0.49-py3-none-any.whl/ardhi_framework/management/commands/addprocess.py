from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Start a new Ardhi sasa process'

    def add_arguments(self, parser):
        parser.add_argument('verbose_name', type=str, help='The full name of the process:')
        parser.add_argument('shortened_name', type=str, help='The shortened name of the process (50 chars or less):')

    def handle(self, *args, **kwargs):
        name = kwargs['shortened_name']
        os.system(f'django-admin startapp {name}')

        # Optional: Add custom views, serializers, urls, etc.
        app_path = os.path.join(os.getcwd(), name)
        with open(os.path.join(app_path, 'views.py'), 'w') as f:
            f.write("""from ardhi_framework.generics import ArdhiGenericViewSet\n\nclass ExampleView(ArdhiGenericViewSet):\n    @custom_view_action(log=True, url_path='my-first-view')\n    def example_view_url(self, request):\n         self.serializer_class=ExampleSerializerClass\n        return self.run_serializer_validator('Success message in the end!')\n""")

        self.stdout.write(self.style.SUCCESS(f'Successfully created a new Ardhi based application: {name}'))




