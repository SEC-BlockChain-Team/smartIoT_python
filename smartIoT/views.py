

from django.http.response import HttpResponse
from django.shortcuts import render
import json
import random
from time import sleep
from .all import func
# Create your views here.


class Data(object):
    def __init__(self, **kwargs):
        for field in ('id', 'temperature', 'humidity', 'smoke', 'gas', 'flame'):
            setattr(self, field, kwargs.get(field, None))


datas = {}


def getMaxDataId():
    if(not datas):
        return 1
    return max(datas)+1


def getTemp():
    return random.random()*100


def getHumidity():
    return random.random()*100


def getSmoke():
    return random.choice(['No Smoke', 'Smoke'])


def getGas():
    return random.choice((['No Gas', 'Gas']))


def getFlame():
    return random.choice(['No Fire', 'Fire'])


def objDict(obj):
    return obj.__dict__


def createData():
    _id = getMaxDataId()
    _temperature = getTemp()
    _humidity = getHumidity()
    _smoke = getSmoke()
    _gas = getGas()
    _flame = getFlame()
    datas[_id] = Data(id=_id, temperature=_temperature,
                      humidity=_humidity, smoke=_smoke, gas=_gas, flame=_flame)
    return datas[_id]


def dumpData(request):
    func()
    data = json.dumps(datas, default=objDict)
    datas.clear()
    # return data;
    return HttpResponse(data)


def homeView(request):
    return render(request, './smartIoT/home.html')
