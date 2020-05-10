from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Thing
from random import random
from time import time
import os, boto3
from boto3.dynamodb.conditions import Key,Attr

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
    time_flies = int(time() - thing.clear_time)
    thing.weight = weight - thing.net_weight
    submitDB(time_flies, thing.weight)
    thing.save()
    return JsonResponse({"status": "success", "action": "submit record"})

def settings(request):
    return HttpResponse("Not avaliable")
    # return render(request, 'linkall/settings.html', context)

def dashboard(request):
    return HttpResponse("Not avaliable")

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