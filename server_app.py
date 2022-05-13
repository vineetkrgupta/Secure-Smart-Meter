# -*- coding: utf-8 -*-
"""
Created on Wed May  4 22:07:43 2022

@author: vk779
"""

from flask import Flask, jsonify, request, make_response, url_for, redirect
import requests, json
import crypto
import json

app = Flask(__name__)


def json_save(msg):
    pass


@app.route('/', methods=['GET', 'POST'])
def default():
    if request.method == 'POST':
        msg = request.get_data()
        # print(msg)
        msg = crypto.decrypt(msg).decode("utf8")
        msg = msg.replace("'", "")
        # msg.replace('"',"")
        # ms
        msg = msg.strip('][').split(', ')
        msg[0] = int(msg[0])
        print(msg)

    return ("The web app is working")


# "<> is used to define parameter which we can pass to our function in this case cube
@app.route('/cube/<int:n>')
def cube(n):
    """return str(int(n)*int(n)* int(n))
    could have been used if we havent specified our parameter type as by default
    string is considered"""
    return str(n * n * n)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000, debug=False)  we could set port and host here
    app.run()  # by default port 5000 is used
