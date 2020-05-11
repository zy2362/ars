import boto3, sys
import numpy as np
from time import time, sleep
from boto3.dynamodb.conditions import Key,Attr
from datetime import datetime
from sklearn.linear_model import LinearRegression

def scan(notification=False):
    phone = "6469193375"
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('linkall')
    response = table.scan(
        FilterExpression=Attr('thing_id').eq(1)
    )
    data = parse(response['Items'])
    if len(data) > 1:
        betas = linearRegression(datas=data, alpha=alpha, iteration=iteration)
        runout_time = int(predict([1,0], betas))
        #remains_time = runout_time - int(time())
        remains_time = datetime.fromtimestamp(runout_time - 4 * 3600)
        if notification == True:
            alert(phone, alarm_type="runout", data=remains_time)
        else:
            return [str(remains_time), data, betas]
            
def predict(thing_id=1,notification=False): # 1 for testing
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('linkall')
    response = table.scan(
        FilterExpression=Attr('thing_id').eq(thing_id)
    )
    X, Y, rawData = parse(response['Items'])
    if len(X) > 1:
        reg = LinearRegression().fit(X, Y)
        runout_time = reg.predict(np.array([[0]]))
        remains_time = datetime.fromtimestamp(runout_time[0] - 4 * 3600)
        return [runout_time[0], rawData, betas]

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
        msg = 'Your water will runout at %s as predicted. Pleas notice.' % data
    elif alarm_type == 'offline':
        msg = 'Your ARS device for is offline'
    a = client.publish(Message = msg, TopicArn = topic_arn)
    #print(a)

if __name__ == "__main__":
    if sys.argv[1] == 'loop':
        while True:
            predict(notification=True)
            sleep(20)
    else:
        predict(notification=True)