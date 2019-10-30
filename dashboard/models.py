import math

from datetime import timedelta
from django.db import models

class Client(models.Model):

    client_id = models.BigIntegerField(primary_key=True, default=0)
    time_spent = models.FloatField(default=0)
    extra_hours = models.IntegerField(default=0)
    sla_hours = models.FloatField(default=0)
    name = models.CharField(
        default="Client Name", max_length=500, verbose_name="Client Name"
    )
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.name!r}, {self.status!r})')

    def hours_remaining(self):
        if self.status() == 'under':
            return float(self.sla_hours) - float(self.time_spent)

        return 0

    def overspend(self):
        if self.status() == 'over':
            return float(self.time_spent) - float(self.sla_hours)

        return

    def status(self):
        if self.sla_hours > 0:
            if float(self.sla_hours) >= float(self.time_spent):
                return 'under'
            return 'over'
        return 'none'

    def time_percentage(self):
        if self.sla_hours > 0 and self.hours_remaining():
            remainder = (
                float(self.hours_remaining()) / float(self.sla_hours)
            ) * 100
            return math.ceil(remainder)

        return 0

    