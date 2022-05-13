from time import time

import flask
from flask import Flask, Markup, render_template, jsonify, request, make_response, url_for, redirect
import secrets
import flask_login
from flask_login import current_user
from pexpect import EOF
import requests, json
import crypto

app = Flask(__name__, template_folder='templates')
app.secret_key = secrets.token_hex(16)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = {"test@gmail.com": {"password": "root"}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('inputEmail')
    if email not in users:
        return
    user = User()
    user.id = email
    return user


pulse = []

time_of_pulse = []

macid = ""


@app.route('/')
def show():
    if current_user.is_authenticated:
        load_data()
        #labels = time_of_pulse
        values = pulse
        total = values[-1]
        #print(todays)
        try:
            current_consumption = values[-1] - values[-10]
        except:
            current_consumption = 0
        global macid
        load_data()
        line_labels = time_of_pulse
        line_values = pulse
        return render_template('index.html', total=total, consumption=current_consumption, user=flask_login.current_user.id,title='Meter reading ' + macid, max=max(pulse) + 20, labels=line_labels,
                                                      values=line_values)
    return render_template('login.html')


@app.route('/data', methods=['GET', 'POST'])
def data_add_route():
    global macid
    if request.method == 'POST':
        msg = request.get_data()
        print("......................................................")
        print(" ")
        print("##.......Here is the Encryted Text Recieved.......##")
        print("")
        print(msg)
        print(" ")
        msg = crypto.decrypt(msg).decode("utf8")
        msg = msg.replace("'", "")
        # msg.replace('"',"")
        # ms
        msg = msg.strip('][').split(', ')
        msg[0] = int(msg[0])
        macid = msg[1]
        print("...The Decrypted Message...")
        print("")
        print(msg)
        print("......................................................")
        # print(" the ")
        # print(msg[0])
        # print(msg[3])
        add_data(msg[0], msg[3])

    return ("The web app is working")


def load_data(file_to_open="data.txt"):
    global pulse, time_of_pulse
    f = open(file_to_open, 'r')

    pulse.clear()
    time_of_pulse.clear()

    while True:
        content = f.readline()
        if not content:
            break
        content = list(content.split(" "))
        pulse.append(float(content[0]))
        time_of_pulse.append((content[1])[:-4])
        # print(content)
    # print(pulse,time_of_pulse)
    f.close()


def add_data(x, y, file_to_open="data.txt"):
    f = open(file_to_open, 'a')
    data = str(x) + " " + str(y) + "\n"
    f.write(data)
    f.close()


@app.route('/line')
def line():
    global macid
    load_data()
    line_labels = time_of_pulse
    line_values = pulse
    return render_template('line_chart.html', title='Meter reading ' + macid, max=max(pulse) + 20, labels=line_labels,
                           values=line_values)


@app.route('/charts.html')
def charts():
    if current_user.is_authenticated:
        global macid
        load_data()
        line_labels = time_of_pulse
        line_values = pulse
        return render_template('charts.html', title='Meter reading ' + macid, max=max(pulse) + 20, labels=line_labels,
                               values=line_values)
    return render_template('login.html')



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return flask.redirect(flask.url_for('show'))
    print(request.form)
    username = request.form['inputEmail']
    password = request.form['inputPassword']
    print(username, password)
    if username == username and password == users[username]['password']:
        user = User()
        user.id = username
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('show'))
    return render_template('401.html')


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('show'))


@app.route('/<page_name>')
def render_page(page_name):
    if current_user.is_authenticated:
        if page_name == 'index':
            return flask.redirect(flask.url_for('show'))
        load_data()
        last_reading = time_of_pulse[len(time_of_pulse) - 1]
        return render_template(page_name, reading=last_reading, user=flask_login.current_user.id)
    return render_template("login.html")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

# source ---> https://blog.ruanbekker.com/blog/2017/12/14/graphing-pretty-charts-with-python-flask-and-chartjs/
