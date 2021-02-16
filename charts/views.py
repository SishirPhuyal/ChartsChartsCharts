from django.shortcuts import render, redirect
from .models import *
from .forms import *
from .tests import *

def home(request):
    charts = Chart.objects.all()

    form = ChartForm()

    if request.method == "POST":
        form = ChartForm(request.POST)
        if form.is_valid():
            form.save()
        chartPic = showChart(charts[len(charts)-1].chart).drawchart()
        context = {"picture": chartPic}
        return render(request, 'index2.html', context)

    context = {"charts": charts, "form": form}
    return render(request, 'index.html', context)

def gallery(request):
    newcharts = newChart.objects.all()

    gallery_storage = []

    for chart in newcharts:
        gallery_storage.append(showChart(chart.symbol, chart.name).drawchart())

    context = {"gallery": gallery_storage}

    return render(request, 'chartsgallery.html', context)
