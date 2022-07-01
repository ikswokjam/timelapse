#!/usr/bin/env python
import math
import os
import sys
import time
from datetime import date, datetime, timedelta, timezone
from os import path, system
from time import sleep

import astral
import astral.sun
import pandas as pd
import pytz
import sunriset
from picamera import PiCamera
from suntime import Sun, SunTimeException
from suntimes import SunTimes

'''Herender geleend no credits to me'''

latitude = 52.3817224501329
longitude = 4.896019458011408
altitude = 0
now = datetime.now()
nowts = datetime.timestamp(now)
camera = PiCamera()
camera.resolution = (1920, 1080)

def progress_wait(count, total, status=''):
    bar_len = total
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(total * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s %s %s\r' % (bar, percents, 'sec', total, status))
    sys.stdout.flush()

def progress_timelapse(count, total, status=''):
    bar_len = 99
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def verschil(date):
    sun = Sun(latitude, longitude)
    today_sr = sun.get_sunrise_time(date)
    today_ss = sun.get_sunset_time(date)
    rise = datetime.timestamp(today_sr)
    set = datetime.timestamp(today_ss)
    if nowts > rise:
        rise = nowts
    else:
        waitingtime = rise - nowts
    delta = set - rise
    return delta


def rounded(tijd):
    roundrise = pd.to_datetime(tijd)
    rounded = roundrise.ceil('min')
    return datetime.timestamp(rounded)

def sunwait(date):
    sun = Sun(latitude, longitude)
    today_sr = sun.get_sunrise_time(date)
    today_ss = sun.get_sunset_time(date)
    rise = datetime.timestamp(today_sr)
    set = datetime.timestamp(today_ss)
    if nowts > rise:
         wait = rounded(now)-nowts
    else:
        wait = rise - nowts
    return int(wait)

def aantaluren():
   uren = (verschil(now))/(60*60)
   return uren

def aantalfotos():
    aantalminwachten = (1) #aantal minuten dat er gewacht moet worden voor de volgende foto
    aantalfotosperuur = round(60/aantalminwachten)
    uren = aantaluren()
    fotos = round(uren*aantalfotosperuur)
    mininterval = round((verschil(now)/fotos)/60)
    tlminutes = int(verschil(now)/60)
    secondsinterval = 60
    numphotos = int((tlminutes*60)/secondsinterval) #number of photos to take
    data = {
        "uren": uren,
        "interval": mininterval,
        "tlminutes": tlminutes,
        "secondeninterval": secondsinterval,
        "numphotos": numphotos
        }
#    print(data)
    return numphotos


#sleep(sunwait(now))

for i in range(sunwait(now)):
    progress_wait(i, sunwait(now))
    sleep(1)

for i in range(aantalfotos()):
    now = datetime.now()
    timestamp = math.ceil(datetime.timestamp(now))
    tegaan = (aantalfotos() - (i+1))
    gedaan = i
    camera.capture('./foto/image{0:10d}.jpg'.format(timestamp))
    tijd = datetime.fromtimestamp(timestamp)
    progress_timelapse(i+1, aantalfotos())
    print ( str(tijd) + " - " + str(i+1) + "/"+ str(aantalfotos()))
    sleep(((aantaluren()*(60*60))/aantalfotos()))

print("Done taking photos.")

