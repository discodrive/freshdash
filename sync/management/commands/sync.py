from sync.models import API
from django.core.management.base import BaseCommand, CommandError
from dashboard.models import Client

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

        parser.add_argument(
            '--fromdate',
            default='',
            help='Specify a start date for retrieving tickets',
        )

    def handle(self, *args, **options):
        api = API('freshdesk')
        params = ''

        if options['perpage']:
            params = '?per_page=' + options['perpage']
        elif options['fromdate']:
            params = '?query=' + options['fromdate']

        if options['endpoint'] == 'companies':
            return api.sync(api.get(options['endpoint'], params))
        elif options['endpoint'] == 'tickets':
            return api.ticket_sync(api.get(options['endpoint'], params))
