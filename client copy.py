import datetime
import os
import re, uuid
import requests
import crypto



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


senddata()
