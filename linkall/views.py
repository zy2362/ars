from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Thing
from random import random
from time import time


def initialize(request):
    thing = Thing(id=1, name = 'Water',
                  net_weight = 184,
                  clear_time = time(),
                  phone      = '6469193375',
                 )
    thing.save()
    return JsonResponse({"status": "success", "action": "initialization"})

def submit(request, weight):
    thing = Thing.objects.get(id=1)
    thing.watch_dog = 0
    if thing.weight <= weight - thing.net_weight:
        f = open('~data/1.csv', 'w')
        thing.clear_time = time()
    else:
        f = open('~/data/1.csv', 'a+')
    time_flies = int(time() - thing.clear_time)
    f.write(str(thing.weight)+","+str(time_flies)+"\n")
    thing.weight = weight - thing.net_weight
    thing.save()
    return JsonResponse({"status": "success", "action": "submit record"})

def settings(request):
    return HttpResponse("Not avaliable")
    # return render(request, 'linkall/settings.html', context)

def dashboard(request, user_id):
    return HttpResponse("Not avaliable")
