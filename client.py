import datetime
import os
import re, uuid
import requests
import crypto

import RPi.GPIO as GPIO
# joins elements of getnode() after each 2 digits.
# using regex expression
#print ("The MAC address in formatted and less complex way is : ", end="")
# mac id in raw format print(uuid.getnode())

count=0


def data_return():
    global count
    macid = (':'.join(re.findall('..', '%012x' % uuid.getnode())))
    current_time = datetime.datetime.now() 
    date = str(current_time.date())
    time = str(current_time.time())
    unit_reading = count
    data = [ unit_reading , str(macid) , date , time ]
    return data







def senddata():
    url= "http://192.168.1.18:5000/data"
    dat = data_return()
    print("....",dat)
    dat = crypto.encrypt(dat)
    print(type(dat))
    #mydata= {'payload' : dat}
    x = requests.post(url , data = dat)
    print(x.text)



 # Import Raspberry Pi GPIO library
def button_callback(channel):
    global count
    count+=1
    senddata()
    print("data was send ")


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback) # Setup event on pin 10 rising edge
message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up

