from sync.models import API
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--endpoint', 
            default='',
            help='Add a freshdesk endpoint', 
        )

    def handle(self, *args, **options):
        api = API('freshdesk')
        return api.sync(api.get(options['endpoint']))
