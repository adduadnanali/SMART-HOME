import sys
import time
import random
import twilio
from twilio.rest import Client

from Adafruit_IO import MQTTClient

import RPi.GPIO as GPIO

account_sid = 'ACfcc61fd909204a0d728b5b6b7088a352'  #account_sid of twilio
auth_token = '48e626cbe9a281155f802df2f1823cb4'     #account_token of twilio
Client = Client(account_sid, auth_token)
ADAFRUIT_IO_KEY = 'aio_iDbs50spMZFLGE7LUvf7hW6HezD5' #adafruit.io account key
ADAFRUIT_IO_USERNAME = 'adduadnanali'                #adafruit.io username


FEED_ID = 'led'
IN1 = 37
IN2 = 35
IN3 = 33
IN4 = 31

ir1 = 38
ir2 = 36
pir = 40
ldr = 24
smoke=22
buzzer1=18
buzzer2=16

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(ir1,GPIO.IN)
GPIO.setup(ir2,GPIO.IN)
GPIO.setup(pir,GPIO.IN)
GPIO.setup(ldr,GPIO.IN)
GPIO.setup(smoke,GPIO.IN)

GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)
GPIO.setup(IN3,GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)


GPIO.setup(buzzer1,GPIO.OUT)
GPIO.setup(buzzer2,GPIO.OUT)

GPIO.output(IN1,True)
GPIO.output(IN2,True)
GPIO.output(IN3,True)
GPIO.output(IN4,True)

GPIO.output(buzzer1,False)
GPIO.output(buzzer2,False)

#sensor = adafruit_dht.DHT11
# called when we're connected to adafruit mqtt server
def connected(client):
    """Connected function will be called when the client is connected to
    Adafruit IO.This is a good place to subscribe to feed changes.  The client
    parameter passed to this function is the Adafruit IO MQTT client so you
    can make calls against it easily.
    """
    # Subscribe to changes on a feed named Counter.
    print('Subscribing to Feed {0}'.format(FEED_ID))
    client.subscribe("led1")
    client.subscribe("led2")
    client.subscribe("led3")
    client.subscribe("led4")
    print('Waiting for feed data...')

#this function will be automatically called, if we're disconnected from adafruit mqtt server
def disconnected(client):
    """Disconnected function will be called when the client disconnects."""
    sys.exit(1)

# this function will be called whenever there is a new data to the feeds to which we've subscribed
def message(client, feed_id, payload):
    """Message function will be called when a subscribed feed has a new value.
    The feed_id parameter identifies the feed, and the payload parameter has
    the new value.
    """
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    print("Actual payload is ",payload)
    if feed_id == 'led1':
        if payload == 'ON':
            print("turn on LED 1 here")
            GPIO.output(IN1,False)
        if payload == 'OFF':
            print("turn Off LED 1 here")
            GPIO.output(IN1,True)
            
    if feed_id == 'led2':
        if payload == 'ON':
            print("turn on LED 2 here")
            GPIO.output(IN2,False)
        if payload == 'OFF':
            print("turn Off LED 2 here")
            GPIO.output(IN2,True)
            
    if feed_id == 'led3':
        if payload == 'ON':
            print("turn on LED 3 here")
            GPIO.output(IN3,False)
        if payload == 'OFF':
            print("turn Off LED 3 here")
            GPIO.output(IN3,True)
            
    if feed_id == 'led4':
        if payload == 'ON':
            print("turn on LED 4 here")
            GPIO.output(IN4,False)
        if payload == 'OFF':
            print("turn Off LED 4 here")
            GPIO.output(IN4,True)


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message

# Connect to the Adafruit IO server.
client.connect()


client.loop_background()

print("Initialzing PIR Sensor......")
time.sleep(5)
print("PIR Ready...")
print(" ")

while True:
    #ldr sensor turn on light everytime when the room is dark
    state=GPIO.input(ldr)
    if state==1:
        GPIO.output(IN3,False)
        print("NO SUNLIGHT,LED-ON by ldr sensor")
        time.sleep(1)
        
    else:
        GPIO.output(IN3,True)
        time.sleep(1)
        
    #ir2 send an sms when we recieve a mail or newspaper
    if GPIO.input(ir2):
        GPIO.output(buzzer2,False)
        
        
    else:
        print("package recieved by ir2 sms sent")
        GPIO.output(buzzer2,True)
        message = Client.messages.create(
          body='!!!!---------------------------------------------------YOU HAVE RECIEVED A PACKAGE PLEASE CHECK BOX --------------------------------------------------------------!!!',
          from_='+18575755527',
          to='+917093565037'
          )
            
        
    #ir1 turn on light when there is an object
    if GPIO.input(ir1):
          GPIO.output(IN4,True)
          
    else:
          GPIO.output(IN4,False)
          print("Object found by ir 1 LED ON")
          time.sleep(1)
          
    #pir sensor used to detect motion and send an sms
    pstate= GPIO.input(pir)
    if pstate==1:
          
          GPIO.output(buzzer1,True)
          print("Motion Detected sms sent ")
          time.sleep(1)
          message = Client.messages.create(
          body='!!!!----------------------------------------------------------WARNINGG THERE IS AN INTRUDER------------------------------------------------------------!!!!!!',
          from_='+18575755527',
          to='+917093565037'
          )
            
    else:
          GPIO.output(buzzer1,False)
                          

"""
while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print('Temp={0}*C  Humidity={1}%'.format(temperature, humidity))
        client.publish('temperature',temperature)
        client.publish('humidity',humidity)
        print("values published")
        time.sleep(60)
    else:
        print("Failed to get reading. Try again")
        """
