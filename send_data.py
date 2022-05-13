# -*- coding: utf-8 -*-
import requests

import crypto

import data_meter



url= "http://127.0.0.1:5000/data"

dat = data_meter.data_return()

print("....",dat)
dat = crypto.encrypt(dat)

print(type(dat))

#mydata= {'payload' : dat}

x = requests.post(url, data = dat)

print(x.text)