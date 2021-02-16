from django import forms
from .models import *

class ChartForm(forms.ModelForm):
    class Meta:
        model = Chart
        fields = '__all__'

