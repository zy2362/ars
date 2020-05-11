import os, boto3, sys
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Thing
from random import random
from time import time, sleep
from datetime import datetime
from boto3.dynamodb.conditions import Key,Attr
from sklearn.linear_model import LinearRegression

#==================================
# Precidt
#==================================

def scan():
    alpha = 0.085
    iteration = 10
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('linkall')
    response = table.scan(
        FilterExpression=Attr('thing_id').eq(1)
    )
    X, Y, rawData = parse(response['Items'])
    if len(X) > 1:
        reg = LinearRegression().fit(X, Y)
        betas = [0,0]
        runout_time = reg.predict(np.array([[0]]))
        #remains_time = datetime.fromtimestamp(runout_time - 4 * 3600)
        return [runout_time[0], rawData, betas]
    else:
        return False

def parse(datas):
    weights = []
    times = []
    rawData = []
    for data in datas:
        weights.append([int(data['weight'])])
        times.append(int(data['time']))
        rawData.append([int(data['time']),int(data['weight'])])
    weights = np.array(weights)
    times = np.array(times)
    return weights, times, rawData

#==================================
#  MODUALS
#==================================

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
        clearDB()
        thing.clear_time = time()
    thing.weight = weight - thing.net_weight
    submitDB(int(time()-thing.clear_time), thing.weight)
    thing.save()
    return JsonResponse({"status": "success", "action": "submit record"})

def settings(request):
    return HttpResponse("Not avaliable")
    # return render(request, 'linkall/settings.html', context)

def dashboard(request):
    thing = Thing.objects.get(id=1)
    data = scan()
    try:
        data = scan()
    except:
        data = [1589152465, [[1,9,1589152465],[1,90,1589162455],[1,80,1589172445,80],[1,70,1589182435,70],[1,50,1589192425,60]],[1589152465,-1] ]
    if data == False:
        return HttpResponse("Data is still collecting...")
    else:
        context = {'user':'Yuan Sa', 'date':datetime.fromtimestamp(data[0]+thing.clear_time-4*3600), 'data':data[1], 'beta':data[2]}
        return render(request, 'linkall/dashboard.html', context=context)

def submitDB(time, weight):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('linkall')
    table.put_item(
        Item={
            'id': time,
            'time': time,
            'weight': weight,
            'thing_id': 1
        }
    )

def clearDB():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('linkall')
    response = table.scan(
        FilterExpression=Attr('thing_id').eq(1)
    )
    items = response['Items']
    for item in items:
        response2 = table.delete_item(
            Key={
                'id': item['id']
            }
        )