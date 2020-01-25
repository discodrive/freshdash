import requests
import os
import math

from datetime import timedelta
from django.db import models
from dashboard.models import Client, TimeSheet, ClientOwner
from dashboard.helpers import month_first_day

class API(models.Model):
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.name!r})')

    def get(self, endpoint: str = '', perpage: str = ''):
        r = requests.get(
            "https://substrakt.freshdesk.com/api/v2/"+ endpoint + perpage,
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
                name=client['name'],
                product_owner=o
            )
            c.save()

            t = TimeSheet(
                client_id=client['id'],
                sla_hours=client['custom_fields']['sla_allowance_hours'], 
                time_spent=self._time_by_client(str(client['id']), str(month_first_day()))
            )
            t.save()

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
