import matplotlib
from django.test import TestCase
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import pandas_datareader as web
from datetime import datetime, timedelta
from collections import Counter
import io
import urllib, base64

# Create your tests here.

def chart_prediction(closing_prices):
  past_moving_avgs = []
  todays_price = closing_prices[-1]
  for i in range(3,21,3):
    ma = create_ma(i,closing_prices)
    past_moving_avgs.append(ma[0])
  directions = []
  for ma in past_moving_avgs:
      directions.append(todays_price - ma.get("close"))
  new_price = todays_price
  future_date = past_moving_avgs[0].get("date")
  new_cordinates = [{"date":future_date,"close":new_price}]
  multiplier = 1
  for num in directions:
    new_cordinates.append({"date":future_date+timedelta(3),"close":new_price+num})
    new_price += num*multiplier
    future_date += timedelta(3)
    multiplier = num/5

  def get_xcordi():
    datalist = []
    for cordinate in new_cordinates:
      datalist.append(cordinate.get("date"))
    return datalist
  def get_ycordi():
    datalist = []
    for cordinate in new_cordinates:
      datalist.append(cordinate.get("close"))
    return datalist
  x_cordi = get_xcordi()
  y_cordi = get_ycordi()
  scaler = max(closing_prices) *.01
  # plt.annotate('Current Price',fontsize=20,xy=(closing_prices.index[-1], closing_prices[-1]), xytext=(closing_prices.index[-1], closing_prices[-1]+scaler),
  #            arrowprops=dict(facecolor='red',alpha=0.3,shrink=1),
  #            )
  # plt.annotate('Short Term',fontsize=20,xy=(x_cordi[2], y_cordi[2]-(.01*scaler)), xytext=(x_cordi[2], y_cordi[2]-(scaler)),
  #            arrowprops=dict(facecolor='green',alpha=0.3,shrink=1)
  #            )
  # plt.annotate('Long Term',fontsize=20,xy=(x_cordi[-1], y_cordi[-1]+(.01*scaler)), xytext=(x_cordi[-1], y_cordi[-1]+(scaler)),
  #            arrowprops=dict(facecolor='blue',alpha=0.3,shrink=1)
  #            )


  circle1 = plt.Circle((closing_prices.index[-1], closing_prices[-1]), scaler, color='red')
  circle2 = plt.Circle((x_cordi[2], y_cordi[2]), scaler, color='dodgerblue')
  circle3 = plt.Circle((x_cordi[-1], y_cordi[-1]), scaler, color='darkgreen')
  fig = plt.gcf()
  ax = fig.gca()
  ax.add_patch(circle1),ax.add_patch(circle2),ax.add_patch(circle3), ax.set_facecolor("black")

  plt.plot(x_cordi,y_cordi, linewidth=8, color="white")

def make_dictionary(closing_prices):
    dates = closing_prices.index
    dates_storage = []
    for each_day in range(1,len(dates)):
      dates_storage.append({"date":(dates[len(dates)-each_day]),"close":(closing_prices[len(dates)-each_day])})
    return dates_storage

#Finding Supports and Resistance
def support_res(closing_prices):

  def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]
  prices = []
  zones = []
  if max(closing_prices)-min(closing_prices) < 2:
    for num in closing_prices:
      prices.append(float(num))
    prices = [item for items, c in Counter(prices).most_common() for item in [items] * c]
  else:
    for num in closing_prices:
      prices.append(int(num))
    prices = [item for items, c in Counter(prices).most_common() for item in [items] * c]
  for i in range(1,4):
    zones.append(prices[0])
    prices = remove_values_from_list(prices,prices[0])
  for zone in zones:
    plt.axhline(y=zone, color='white',linewidth=3,linestyle='dashed',alpha=0.3)


def create_ma(day_inc,closing_prices):
  dates_storage = make_dictionary(closing_prices)
  increment = int(len(dates_storage)/day_inc)
  new_dates_storage = dates_storage
  storage = []
  #repeats loop based on total days and desired increments
  for i in range(1,increment+1):
    get_sum = new_dates_storage[:day_inc]
    new_dates_storage = new_dates_storage[day_inc:]
    price = 0
    for x in get_sum:
      price += float(x.get("close"))
    price = price/day_inc
    if len(get_sum) > 1:
      storage.append({"date": (get_sum[0].get("date")),"close": price})
  return(storage)


def plot_ma(increment, closing_prices):
    ma_dataset = create_ma(increment, closing_prices)

    def get_xcordi():
        datalist = []
        for cordinate in ma_dataset:
            datalist.append(cordinate.get("date"))
        return datalist

    def get_ycordi():
        datalist = []
        for cordinate in ma_dataset:
            datalist.append(cordinate.get("close"))
        return datalist

    plt.plot(get_xcordi(), get_ycordi(), linewidth=3, linestyle=':')


class showChart():
    def __init__(self,symbol,name=1):
        self.symbol = symbol
        if name == 1:
            self.name = self.symbol
        else:
            self.name = name
    # Get closing price

    def drawchart(self):
        df = web.DataReader(self.symbol, "yahoo", "2021-01-01", datetime.now())
        closing_prices = df['Close']
        plt.figure(figsize=(25,10))
        plt.title(self.name,fontsize=40)
        plt.plot(closing_prices,linewidth=10)
        plot_ma(3,closing_prices)
        plot_ma(5,closing_prices)
        plot_ma(10,closing_prices)
        support_res(closing_prices)
        chart_prediction(closing_prices)
        plt.ylabel('Close Price USD ($)',fontsize=25)
        fig = plt.gcf()

        # PIC converter
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        return uri

