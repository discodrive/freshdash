import requests
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--endpoint', 
            default='',
            help='Add a freshdesk endpoint', 
        )

    def handle(self, *args, **options):
        r = requests.get(
            'https://substrakt.freshdesk.com/api/v2/'+ options['endpoint'],
            # authentication needs to come from env
            auth=("5TZvLFZ9pqTpCtdw1C", "x")
        )
        
        if r.status_code == 200:
            return r.json()

        return False