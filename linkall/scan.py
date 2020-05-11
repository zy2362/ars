import boto3, sys
import numpy as np
from time import time, sleep
from boto3.dynamodb.conditions import Key,Attr
from datetime import datetime
from sklearn.linear_model import LinearRegression
            
def scan(thing_id=1, notification=False): # 1 for testing
    phone = "6469193375"
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('linkall')
    response = table.scan(
        FilterExpression=Attr('thing_id').eq(thing_id)
    )
    X, Y = parse(response['Items'])
    if len(X) > 1:
        reg = LinearRegression().fit(X, Y)
        runout_time = reg.predict(np.array([[0]]))
        if runout_time < time() + 3600 - 4 * 3600:
            runout_time = datetime.fromtimestamp(runout_time[0] - 4 * 3600)
            alert(phone, alarm_type="runout", data=runout_time)

def parse(datas):
    weights = []
    times = []
    for data in datas:
        weights.append([int(data['weight'])])
        times.append(int(data['time']))
    weights = np.array(weights)
    times = np.array(times)
    return weights, times

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