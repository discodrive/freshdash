from sync.models import GoogleDrive
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, *args, **options):
        api = GoogleDrive('Client Spreadsheet')
        return api.spreadsheet()
