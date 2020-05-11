import os, boto3, sys
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Thing
from random import random
from time import time, sleep
from datetime import datetime
from boto3.dynamodb.conditions import Key,Attr

#==================================
# Precidt
#==================================

def scan():
    alpha = 0.000001
    iteration = 2000
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('linkall')
    response = table.scan(
        FilterExpression=Attr('thing_id').eq(1)
    )
    data, rawData = parse(response['Items'])
    if len(data) > 1:
        betas = linearRegression(datas=data, alpha=alpha, iteration=iteration)
        runout_time = int(predict([1,0], betas))
        #remains_time = datetime.fromtimestamp(runout_time - 4 * 3600)
        return [runout_time, rawData, betas]
    else:
        return False

def parse(datas):
    weights = []
    times = []
    for data in datas:
        weights.append(int(data['weight']))
        times.append(int(data['time']))
    weights_std = np.std(weights, ddof=1)
    weights_mean = np.mean(weights)

    parsedData = []
    rawDatas = []
    for data in datas:
        nvRow = [1]
        rawData = [1]
        nvRow.append((int(data['weight']) - weights_mean) / weights_std)
        nvRow.append(int(data['time']))
        rawData.append(int(data['weight']))
        rawData.append(int(data['time']))
        parsedData.append(nvRow)
        rawDatas.append(rawData)

    return parsedData, rawDatas

def linearRegression(datas, alpha, iteration):
    betas = [datas[0][0], datas[0][1] - datas[1][1]]
    for _ in range(iteration):
        tempSum = [0, 0]
        for data in datas:
            tempPredict = predictDelta(data, betas)
            tempSum[0] += tempPredict * data[0]
            tempSum[1] += tempPredict * data[1]
        betas[0] -= alpha * tempSum[0] / len(datas)
        betas[1] -= alpha * tempSum[1] / len(datas)
    return betas

def predictDelta(data, betas):
    return data[0] * betas[0] + data[1] * betas[1] - data[2]

def predict(data, betas):
    return data[0] * betas[0] + data[1] * betas[1]

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
    submitDB(int(time()), thing.weight)
    thing.save()
    return JsonResponse({"status": "success", "action": "submit record"})

def settings(request):
    return HttpResponse("Not avaliable")
    # return render(request, 'linkall/settings.html', context)

def dashboard(request):
    try:
        data = scan()
    except:
        data = [1589152465, [[1,100,1589152465],[1,90,1589162455],[1,80,1589172445,80],[1,70,1589182435,70],[1,50,1589192425,60]],[1589152465,-1] ]
    if data == False:
        return HttpResponse("Data is still collecting...")
    else:
        context = {'user':'Yuan Sa', 'date':datetime.fromtimestamp(data[0]), 'data':data[1], 'beta':data[2]}
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