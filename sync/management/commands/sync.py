from sync.models import API
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--endpoint',
            default='',
            help='Add a freshdesk endpoint', 
        )

        parser.add_argument(
            '--perpage',
            default='',
            help='Specify a number of items per page', 
        )

    def handle(self, *args, **options):
        api = API('freshdesk')
        perpage = ''

        if options['perpage']:
            perpage = '?per_page=' + options['perpage']
            
        return api.sync(api.get(options['endpoint'], perpage))
