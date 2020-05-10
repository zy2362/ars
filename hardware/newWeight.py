import RPi.GPIO as GPIO
import time
import thread
import requests

def toWeight(value):
    return (value-16749000-6875.4) / 103.09

def sample(url):
    # init
    GPIO.setmode(GPIO.BOARD)
    SCK = 13
    SDA = 15
    GPIO.setup(SCK, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(SDA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # start
    sumw = 0
    length_sum = 10
    pos = 0
    while True:
        value = 0
        GPIO.output(SCK, 0)
        while GPIO.input(SCK):
		continue
        while GPIO.input(SDA):
		continue
        time.sleep(1e-6)
        for i in range(24):
            GPIO.output(SCK, 1)
            while 0 == GPIO.input(SCK):
                time.sleep(1e-6)
            value *= 2
            GPIO.output(SCK, 0)
            while GPIO.input(SCK):
		continue
            if GPIO.input(SDA):
                value += 1
        GPIO.output(SCK, 1)
        GPIO.output(SCK, 0)
        
        if value < 1e6:
            value += 16777216
        sumw += toWeight(value)
        pos += 1
        if pos == length_sum:
            pos = 0
            res = int(sumw/float(length_sum))
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
    url = 'http://34.227.157.139:8000'
    while True:
        try:
            thread.start_new_thread(sample, (url,))
            time.sleep(30)
        except:
            print("Error: cannot start a thread")
            
main()