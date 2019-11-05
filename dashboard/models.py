import math

from datetime import timedelta
from django.db import models
from dashboard.helpers import week_of_month


class Client(models.Model):
    
    client_id = models.BigIntegerField(primary_key=True, default=0)
    extra_hours = models.IntegerField(default=0)
    name = models.CharField(
        default="Client Name", max_length=500, verbose_name="Client Name"
    )
    project_owner = models.CharField(
        default="No owner", max_length=100, verbose_name="Project Owner"
    )
    sla_hours = models.FloatField(default=0)
    time_spent = models.FloatField(default=0)
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.name!r}, {self.status!r})')

    def hours_remaining(self):
        return float(self.sla_hours) - float(self.time_spent)

    def hours_remaining_label(self):
        hours = self.hours_remaining()
        
        if hours < 0:
            return f"{abs(hours)} hours over"
        else:
            return f"{hours} hours remaining"


    def status(self):
        h = self.sla_hours
        p = self.time_percentage()

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

    def time_percentage(self):
        if self.sla_hours > 0 and self.hours_remaining() > 0:
            remainder = (
                float(self.hours_remaining()) / float(self.sla_hours)
            ) * 100
            return math.ceil(remainder)

        return 0

    