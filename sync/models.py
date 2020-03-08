import requests
import os
import math
import gspread

from datetime import timedelta, date, datetime
from django.utils.text import slugify
from django.conf import settings
from django.db import models
from oauth2client.service_account import ServiceAccountCredentials
from dashboard.models import Client, TimeSheet, ClientOwner, Ticket
from dashboard.helpers import month_first_day, month_last_day

class API(models.Model):
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.name!r})')

    def get(self, endpoint: str = '', params: str = ''):
        r = requests.get(
            "https://substrakt.freshdesk.com/api/v2/"+ endpoint + params,
            auth=(os.getenv("FRESHDESK_AUTH"), "x")
        )
        
        if r.status_code == 200:
            return r.json()

        return False

    def sync(self, request):
        for client in request:
            # The sla_hours field is an integer so we need to convert None to 0
            if client['custom_fields']['sla_allowance_hours'] is None:
                client['custom_fields']['sla_allowance_hours'] = 0

            if client['custom_fields']['client_owner'] is None:
                client['custom_fields']['client_owner'] = 'No owner'

            if client['custom_fields']['sla_allowance_hours'] == 'tbc':
                client['custom_fields']['sla_allowance_hours'] = 0

            print(f"Importing {client['name']}")

            try:
                o = ClientOwner.objects.get(name=client['custom_fields']['client_owner'])
            except:
                o = ClientOwner(
                    name=client['custom_fields']['client_owner']
                )
                o.save()
                            
            c = Client(
                client_id=client['id'], 
                location=client['custom_fields']['country'],
                name=client['name'],
                product_owner=o,
                slug=slugify(client['name']),
                ticketing_system=client['custom_fields']['ticketing_system'],
                url=client['custom_fields']['live_site_url']
            )
            c.save()

            t = TimeSheet(
                client_id=client['id'],
                sla_hours=client['custom_fields']['sla_allowance_hours'], 
                time_spent=self._time_by_client(str(client['id']), str(month_first_day())),
                import_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            t.save()

    def ticket_sync(self, request):
        for ticket in request:

            try:
                ticket = Ticket.objects.get(id=ticket['id'])
            except:
                print(f"{ticket['subject']}")

                ticket = Ticket(
                    id=ticket['id'],
                    client_id=ticket['company_id'],
                    date=ticket['created_at'],
                    priority=ticket['priority'],
                    status=ticket['status'],
                    subject=ticket['subject']
                )
                ticket.save()

    def _time_by_client(self, client_id: str, start_time: str = ''):
        """Returns total tracked for for a client converted to minutes"""
        r = self.get(
            f"time_entries?company_id={client_id}&executed_after={start_time}"
        )
        total = 0

        for t in self._time_spent(r):
            total = total + timedelta(
                hours=int(t[0:2]),
                minutes=int(t[3:])
            ).seconds

        return round(total / 3600, 1)

    def _time_spent(self, time):
        """Adds all tracked time for a client"""
        tracked_time = []
        if time:
            for time_spent in time:
                tracked_time.append(time_spent.get('time_spent', 0))

        return tracked_time

class GoogleDrive(models.Model):
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.name!r})')

    def spreadsheet(self):
        scope = ['https://spreadsheets.google.com/feeds']
        json = os.path.join(str(settings.STATICFILES_DIRS), '/dashboard/build/json/', 'client_secret.json')
        creds = ServiceAccountCredentials.from_json_keyfile_name(json, scope)
        client = gspread.authorize(creds)

        sheet = client.open("Substrakt - Client Services Maintenance").sheet1

        list_of_hashes = sheet.get_all_records()
        print(list_of_hashes)
