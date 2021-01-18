import math
import datetime

from datetime import timedelta, datetime
from django.db import models
from django.utils import timezone
from dashboard.helpers import week_of_month


class ClientOwner(models.Model):

    name = models.CharField(default="No owner", max_length=100)

    def __str__(self):
        return self.name


class Client(models.Model):
    
    client_id = models.BigIntegerField(primary_key=True, default=0)
    location = models.CharField(default=None, max_length=500, verbose_name="Location", null=True)
    name = models.CharField(default="Client Name", max_length=500, verbose_name="Client Name")
    product_owner = models.ForeignKey(ClientOwner, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(default="client-slug", max_length=50)
    ticketing_system = models.CharField(default=None, max_length=500, verbose_name="Ticketing System", null=True)
    url = models.URLField(default=None, null=True)
    wp_version =  models.CharField(default=None, max_length=500, verbose_name="Wordpress Version", null=True)
    attendable_version = models.CharField(default=None, max_length=500, verbose_name="Attendable Version", null=True)
    onsale_version = models.CharField(default=None, max_length=500, verbose_name="Onsale Version", null=True)
    baseproject = models.BooleanField(default=False)
    event_sync = models.CharField(default=None, max_length=500, verbose_name="Events and Instances Sync", null=True)
    availability_sync =  models.CharField(default=None, max_length=500, verbose_name="Availability Sync", null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.name!r}, {self.status!r})')


    def status(self):
        h = self.time().sla_hours
        p = self.time().time_percentage()

        if h > 0:
            if (p <= 50) and (p > 15) and week_of_month() > 2:
                return 'warning'
            elif (p >= 25) and (p > 0) and week_of_month() > 2:
                return 'critical'
            elif (p <= 15) and (p > 0):
                return 'fine'
            elif (p == 0):
                return 'pause'
        return 'default' 

    def time(self):
        return TimeSheet.objects.get(client_id=self.client_id)

    def owner(self):
        o = ClientOwner.objects.get(client=self.client_id)

        return o.name

class Lighthouse(models.Model):

    def __str__(self):
        return self.date

class Ticket(models.Model):

    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(default=timezone.now)
    priority = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    subject = models.CharField(default="Subject", max_length=500, verbose_name="Subject")


    def __str__(self):
        return self.subject

    def priorityLabel(self):
        return {
            1: 'low',
            2: 'medium',
            3: 'high',
            4: 'urgent'   
        }.get(self.priority, 'None')

    def statusLabel(self):
        return {
            2: 'Open', 
            3: 'Pending',
            4: 'Resolved',
            5: 'Closed'
        }.get(self.status, 'None')


class TimeSheet(models.Model):

    client = models.ForeignKey(Client, primary_key=True, default=0, on_delete=models.CASCADE)
    leftover_hours = models.IntegerField(default=0)
    extra_hours = models.IntegerField(default=0)
    sla_hours = models.FloatField(default=0)
    time_spent = models.FloatField(default=0)
    import_date = models.DateTimeField(default=timezone.now)

    def hours_remaining(self):
        total = float(self.sla_hours) - float(self.time_spent)

        if (self.extra_hours):
            return total + self.extra_hours

        return total

    def hours_remaining_label(self):
        hours = self.hours_remaining()
        
        if hours < 0:
            return f"{abs(hours)} hours over"
        else:
            return f"{hours} hours remaining"

    def sla_hours_label(self):
        return self.sla_hours + self.extra_hours

    def time_percentage(self):
        if self.sla_hours > 0 and self.hours_remaining() > 0:
            remainder = (
                float(self.hours_remaining()) / float(self.sla_hours)
            ) * 100
            return math.ceil(remainder)

        return 0
