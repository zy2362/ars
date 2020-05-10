from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import User, Thing
from random import random
from time import time
from .library import predict

def alarm():
    pass

def initialize(request):
    thing = Thing(id=1, name='Water', net_weight=184, phone='6469193375')
    thing.save()
    return HttpResponse("Initialization successed!")

def submit(request, weight):
    thing = Thing.objects.get(id=1)
    thing.watch_dog = 0
    if thing.weight <= weight - thing.net_weight:
        f = open('~data/1.csv', 'w')
    else:
        f = open('~/data/1.csv', 'a+')
    now = int(time() - 1589083224)
    f.write(str(now),str(thing.weight))
    thing.weight = weight - thing.net_weight
    thing.save()
    if(predict() < 30): # when will alarm user runout
        alarm()
    return JsonResponse({"status":"success"})

def settings(request):
    things = Thing.objects.all()
    user = User.objects.get(id=1)
    context = {'user': user, 'things': things}
    return render(request, 'linkall/settings.html', context)

def dashboard(request, user_id):
    return render(request, 'linkall/dashboard.html', context)
