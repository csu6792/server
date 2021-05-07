#!/usr/bin/env python
import os
from flask import Flask, render_template, Response,request,jsonify,session,redirect
import json
import socket
from datetime import timedelta
from rpiserver import Streamer

from time import sleep
from datetime import datetime


# import camera driver
'''if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera'''

# Raspberry Pi camera module (requires picamera package)
#from camera_pi import Camera

#from camera_opencv import Camera
app = Flask(__name__)


streamer = Streamer('0.0.0.0', 7001)
streamer.start()

app.secret_key = "csu"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)



@app.route('/login', methods=["GET","POST"])
def login():
    if request.method == 'GET':
        return render_template('login2.html')

    data = json.loads(request.form.get('data'))
    user = data['user_id']
    pwd = data['password']
    #user = request.form.get('user')   
    #form的表单提交的数据request.form 类似于post请求request.args 类似django的request.get
    #pwd = request.form.get('pwd')
 
    if user =='admin' and pwd=='admin':
        session['user'] = user
        #return redirect('/home')
        return jsonify('ok')
    #return render_template('login.html',error="用户名错误")
    return jsonify('err')

@app.route("/logout")
def logout():
    # 删除session数据
    session.pop("user", None)
    # 返回登录页面
    return redirect("/login")

@app.route('/')
def index():
    """Video streaming home page."""
    user = session.get('user')
    if not user:
        return redirect('/login')
    return render_template('main.html')

@app.route('/upload', methods=["POST","GET"])
def upload():
    data = json.loads(request.form.get('data'))
    print(data['username'])
    streamer.sendmessage(data['username'])
    return jsonify(data['username'])

@app.route('/upload_check', methods=["GET","POST"])
def upload_check():
    if request.method == "POST":
        try:
            streamer.sendmessage('sent')
            return jsonify('sent')
        except:
            return jsonify('sent')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 8080, threaded=True)
