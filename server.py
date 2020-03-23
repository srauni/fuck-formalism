import requests
import json
import time
from flask import Flask, request, redirect, url_for, send_from_directory, abort, jsonify
from gevent.pywsgi import WSGIServer


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    html = None
    with open('html/index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    return html

@app.route('/fuck-formalism', methods=['POST'])
def get_token():
    try:
        token = request.form['token']
        token = token.strip('"')
        token = token.strip("'")
        if token == '' or token == None:
            return '请填写token再提交'
        token_list = None
        try:
            with open('token.json', 'r') as f:
                token_list = json.loads(f.read())
        except FileNotFoundError:
            token_list = []
        if token in token_list:
            return '您的token已托管，不必重复提交'
        token_list.append(token)
        with open('token.json', 'w') as f:
            f.write(json.dumps(token_list))
        return '成功托管您的token'
    except Exception:
        return '服务器内部错误：' + Exception

@app.route('/example.png', methods=['POST', 'GET'])
def get_img():
    img = None
    with open('html/example.png', 'rb') as f:
        img = f.read()
    return img

@app.route('/status', methods=['POST', 'GET'])
def get_status():
        # 读取今日已填token
        localtime = time.localtime(time.time())
        success_token = None
        try:
            with open(str(localtime.tm_year) + '-' + str(localtime.tm_mon) + '-' + str(localtime.tm_mday) + '.json', 'r') as f:
                success_token = json.loads(f.read())
        except FileNotFoundError:
            success_token = []

        # 读取所有托管token
        all_token = None
        try:
            with open('token.json', 'r') as f:
                all_token = json.loads(f.read())
        except FileNotFoundError:
            all_token = []

        # 读取所有失效token
        useless_token = None
        try:
            with open('useless_token.json', 'r') as f:
                useless_token = json.loads(f.read())
        except FileNotFoundError:
            useless_token = []

        return '已托管' + str(len(all_token)) + '个token；今日已打卡' + str(len(success_token)) + '个；待打卡' + str(len(all_token) - len(useless_token) - len(success_token)) + '个；无效token有' + str(len(useless_token)) + '个。'

if __name__ == "__main__":
    key_path = None
    pem_path = None
    #WSGIServer(('0.0.0.0', 2000), app, keyfile=key_path, certfile=pem_path).serve_forever()
    WSGIServer(('0.0.0.0', 2000), app).serve_forever()
