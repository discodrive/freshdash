import math
import datetime

from datetime import timedelta, datetime
from django.db import models
from dashboard.helpers import week_of_month


class ClientOwner(models.Model):

    name = models.CharField(default="No owner", max_length=100)

    def __str__(self):
        return self.name


class Client(models.Model):
    
    client_id = models.BigIntegerField(primary_key=True, default=0)
    name = models.CharField(default="Client Name", max_length=500, verbose_name="Client Name")
    product_owner = models.ForeignKey(ClientOwner, on_delete=models.SET_NULL, null=True)
    
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


class TimeSheet(models.Model):

    client = models.ForeignKey(Client, primary_key=True, default=0, on_delete=models.CASCADE)
    leftover_hours = models.IntegerField(default=0)
    extra_hours = models.IntegerField(default=0)
    sla_hours = models.FloatField(default=0)
    time_spent = models.FloatField(default=0)
    import_date = models.DateTimeField(default=datetime.now())

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
