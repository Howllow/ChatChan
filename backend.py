# -*- coding:utf-8 _*-
"""
@author:howllow(jinqingzhe)
@file: backend.py
@time: 2019/1/9
@contact: 1600012896@pku.edu.cn

"""
from flask import *
from flask_socketio import *
from db.mydb import *
from db.config import *
import user
import json
import flask_login as fl

app = Flask(__name__)
login_manager = fl.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'please login!'
login_manager.session_protection = 'strong'

app.config['SECRET_KEY'] = 'chatchan'

password = ""
db = pymysql.connect(**config)

@app.route('/')
def homepage():
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        data = request.get_json()
        data['account'] = data.pop('username')
        print(data)
        res = dict()
        reg_message = register_user(data, db)

        if reg_message == 'success':
            res['response_code'] = 0

        elif reg_message == 'duplicate':
            res['response_code'] = 1

        else:
            res['response_code'] = 2

        return json.dumps(res)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        data = request.get_json()
        data['account'] = data.pop('username')
        log_message = login_user(data, db)
        res = dict()

        if log_message == 'success':
            usr = user.User()
            usr.username = data['account']
            usr.id = data['account']
            fl.login_user(usr)
            flash('Login Success')
            res['response_code'] = 0

        elif log_message == 'account not found':
            res['response_code'] = 1

        else:
            res['response_code'] = 2

        return json.dumps(res)


@app.route('/home', methods=['GET'])
@fl.login_required
def home():
    if request.method == 'GET':
        print(fl.current_user.username)
        return render_template('home.html')


@app.route('/room/msg', methods=['GET'])
@fl.login_required
def get_msg():
    data = request.get_json()
    res = dict()
    res['msg_list'] = get_messages_from_room_name(data, db)
    res['response_code'] = 0
    return json.dumps(res)


@app.route('/create_room', methods=['POST'])
@fl.login_required
def new_room():
    data = request.get_json()
    res = dict()
    prefix = '[G]'
    data['roomname'] += prefix
    flag = create_chatroom(data, db)

    if flag == 'success':
        res['response_code'] = 0

    elif flag == 'duplicate':
        res['response_code'] = 1

    else:
        res['response_code'] = 2

    return json.dumps(res)


@app.route('/user/roomlist', methods=['POST', 'GET'])
@fl.login_required
def recent_room():
    if request.method == 'POST':
        res = dict()
        data = request.get_json()
        usrname = data['username']
        lst = get_room_by_name(usrname)
        res['roomlist'] = lst
        res['response_code'] = 0
        return json.dumps(res)


@app.route('/setpassword', methods=['POST', 'GET'])
@fl.login_required
def usr_set():
    if request.method == 'GET':
        return render_template('setting.html')
    elif request.method == 'POST':
        res = dict()
        data = request.get_json()
        res['response_code'] = change_pwd(data, db)
        return json.dumps(res)


@app.route('/room/search', methods=['POST', 'GET'])
@fl.login_required
def room_search():
    if request.method == 'GET':
        return render_template('find.html')
    elif request.method == 'POST':
        res = dict()
        data = request.get_json()
        typ = data['type']
        keyword = data['keyword']
        res['response_code'] = 1
        if typ == 'room':
            res['roomlist'] = find_room(keyword, db)
            res['response_code'] = 0
        else:
            res['userlist'] = find_user(keyword, db)
            res['response_code'] = 0

        return json.dumps(res)


@app.route('/user/myroom', methods=['GET'])
@fl.login_required
def my_room():
    if request.method == 'GET':
        usrname = fl.current_user.username
        lsts = get_room_by_name(usrname)
        rooms = []
        for i in range(len(lsts)):
            lst = lsts[i]
            roomname = lst[0]
            if roomname[0:3] == '[G]':
                rooms.append(roomname)
        return render_template('chatroom.html', roomlist=rooms)


@app.route('/room/newroom', methods=['GET', 'POST'])
@fl.login_required
def new_room:
    if request.method == 'GET':
        return render_template('new.html')


@app.route('/user/send', methods=['POST'])
@fl.login_required
def send_msg():
    data = request.get_json()
    data['account'] = fl.current_user.username
    data['message'] = data.pop('msg')
    res = dict()
    suc = send_message(data, db)
    if suc == 'success':
        res['response_code'] = 0
    else:
        res['response_code'] = 1

    return json.dumps(res)


@app.route('/user/logout', methods=['POST', 'GET'])
@fl.login_required
def logout():
    fl.logout_user()
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return user.UserManager.get(user_id)


if __name__ == '__main__':
    app.run(host='localhost', port='5000')

