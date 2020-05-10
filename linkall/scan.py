import boto3
import numpy as np
from time import time, sleep
from boto3.dynamodb.conditions import Key,Attr
from datetime import datetime

def scan():
    alpha = 0.085
    iteration = 100
    phone = "6469193375"
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('linkall')
    response = table.scan(
        FilterExpression=Attr('thing_id').eq(1)
    )
    data = parse(response['Items'])
    if len(data) > 1:
        betas = linearRegression(datas=data, alpha=alpha, iteration=iteration)
        runout_time = dt_object = datetime.fromtimestamp(int(predict([1,0], betas)))
        remains_time = runout_time - int(time())
        alert(phone, alarm_type="runout", data=runout_time) # for test
        #if remains_time < 30: # should be 3600 * 24 * 3 in final product
        #    alert(phone, alarm_type="runout", data=remains_time)

def parse(datas):
    weights = []
    times = []
    for data in datas:
        weights.append(int(data['weight']))
        times.append(int(data['time']))
    weights_std = np.std(weights, ddof=1)
    weights_mean = np.mean(weights)

    parsedData = []
    for data in datas:
        nvRow = [1]
        nvRow.append((int(data['weight']) - weights_mean) / weights_std)
        nvRow.append(int(data['time']))
        parsedData.append(nvRow)

    return parsedData

def linearRegression(datas, alpha, iteration):
    betas = [0, 0]
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

def alert(phone, alarm_type, data):
    client = boto3.client('sns')
    topic_arn = "arn:aws:sns:us-east-1:154204703882:linkall"
    client.subscribe(
        TopicArn = topic_arn,
        Protocol = 'email',
        Endpoint = 'yuansasi@outlook.com'
    )
    msg = 'You have a new message.'
    if alarm_type == 'runout':
        msg = 'Your water will runout in %s days' % data
    elif alarm_type == 'offline':
        msg = 'Your ARS device for is offline'
    a = client.publish(Message = msg, TopicArn = topic_arn)
    print(a)

if __name__ == "__main__":
    scan()