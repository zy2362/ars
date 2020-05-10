import csv, boto3
import numpy as np
from time import time, sleep

def scan():
    alpha = 0.085
    iteration = 100
    phone = "6469193375"
    with open('~/data/1.csv') as f:
        data = parse(csv.reader(f))
        if len(data) > 1:
            betas = linearRegression(datas=data, alpha=alpha, iteration=iteration)
            runout_time = predict([1,0], betas)
            remains_time = runout_time - time()
            alert(phone, alarm_type="runout", data=remains_time) # for test
            #if remains_time < 30: # should be 3600 * 24 * 3 in final product
            #    alert(phone, alarm_type="runout", data=remains_time)

def parse(data):
    weights = []
    times = []
    for row in data:
        weights.append(int(row[1]))
        times.append(int(row[0]))
    weights_std = np.std(weights, ddof=1)
    weights_mean = np.mean(weights)

    parsedData = []
    for row in data:
        nvRow = [1]
        nvRow.append((int(row) - weights_mean) / weights_std)
        nvRow.append(int(row[-1]))
        parsedData.append(nvRow)

    return parsedData

def linearRegression(datas, alpha, iteration):
    betas = [0, 0]
    for _ in range(iteration):
        tempSum = [0, 0]
        for data in datas:
            tempPredict = predict(data, betas)
            tempSum[0] += tempPredict * data[0]
            tempSum[1] += tempPredict * data[1]
        betas[0] -= alpha * tempSum[0] / len(datas)
        betas[1] -= alpha * tempSum[1] / len(datas)
    return betas

def predict(data, betas):
    return data[0] * betas[0] + data[1] * betas[1] - data[2]

def alert(phone, alarm_type, data):
    client = boto3.client('sns')
    topic_arn = "arn:aws:sns:us-east-1:154204703882:mtaSub"
    client.subscribe(
        TopicArn = 'linkall',
        Protocol = 'sms',
        Endpoint = '+1' + phone
    )
    msg = 'You have a new message.'
    if alarm_type == 'runout':
        msg = 'Your %s will be runout in %s days' % data
    elif alarm_type == 'offline':
        msg = 'Your ARS device for is offline'
    client.publish(Message = msg, TopicArn = topic_arn)

if __name__ == "__main__":
    scan()