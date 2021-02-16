from django.db import models
from .tests import *


class Chart(models.Model):
    chart = models.CharField(max_length=120)
    def __str__(self):
        return self.chart
class newChart(models.Model):
    symbol = models.CharField(max_length=120)
    name = models.CharField(max_length=120)