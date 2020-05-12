# Group YJZY
# Author: Yanwen yj2556
# IoT Spring2020 final project

import RPi.GPIO as GPIO
import time
import thread
import requests

def toWeight(value):
    return (value-16749000-6875.4) / 103.09 # by linearly fitting. Unit: gram

def sample(url):
    # init
    GPIO.setmode(GPIO.BOARD) # using Board instead of BCM
    SCK = 13 # sending clock to ADC
    SDA = 15 # receiving data from ADC
    GPIO.setup(SCK, GPIO.OUT, initial=GPIO.LOW) # if the clock is high for a while, the ADC may reset itself
    GPIO.setup(SDA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # start
    sumw = 0
    length_sum = 10 # using average value as the final output. Sample for 10 times in 1 second
    pos = 0
    while True:
        value = 0
        GPIO.output(SCK, 0)
        while GPIO.input(SCK):
		continue
        while GPIO.input(SDA): # wait for data's fallen edge
		continue
        time.sleep(1e-6)
        for i in range(24): # 24-bit data
            GPIO.output(SCK, 1)
            while 0 == GPIO.input(SCK):
                time.sleep(1e-6)
            value *= 2 # AKA value = value << 1
            GPIO.output(SCK, 0)
            while GPIO.input(SCK):
		continue
            if GPIO.input(SDA):
                value += 1
        GPIO.output(SCK, 1) # an extra pulse telling the ADC to use channel A and gain 128 in next sampling
        GPIO.output(SCK, 0)
        
        if value < 1e6: # when out of range the output of adc will go back to 0
            value += 16777216
        sumw += toWeight(value)
        pos += 1
        if pos == length_sum:
            pos = 0
            res = int(sumw/float(length_sum)) # for the request url, the weight has to be an integer
            if res < 0:
               res = 0
               print "Invalid weight value detected!"
            print("The weight of object is %d g" % res)
            req = requests.get(url + '/linkall/submit/' +str(res))
            print("The message from the web is: " + req.content)
            return res
            sumw = 0
        time.sleep(1/float(length_sum))


def main():
    url = 'http://34.227.157.139:8000' # our front-end website
    while True:
        try:
            thread.start_new_thread(sample, (url,)) # using a new thread to do the measurement
            time.sleep(30) # for demo only. In real situation the sample may happen only once a day for each container
        except:
            print("Error: cannot start a thread")
            
main()