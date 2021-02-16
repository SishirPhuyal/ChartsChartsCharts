from django.contrib import admin

from .models import *

class ChartsAdmin(admin.ModelAdmin):
    class Meta:
        model = Chart

class displayChartsAdmin(admin.ModelAdmin):
    class Meta:
        model = newChart


admin.site.register(Chart,ChartsAdmin)
admin.site.register(newChart,displayChartsAdmin)