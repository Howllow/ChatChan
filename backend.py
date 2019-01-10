# -*- coding:utf-8 _*-
"""
@author:howllow(jinqingzhe)
@file: backend.py
@time: 2019/1/9
@contact: 1600012896@pku.edu.cn

"""
from flask import *
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
db1 = pymysql.connect(**config)
db2 = pymysql.connect(**config)


@app.route('/')
def homepage():
    return redirect(url_for('home'))


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
        return render_template('home.html')


@app.route('/room/msg', methods=['GET', 'POST'])
@fl.login_required
def get_msg():
    db3 = pymysql.connect(**config)
    data = request.get_json()
    res = dict()
    data['room_name'] = data.pop('roomname')
    res['msglist'] = get_messages_from_room_name(data, db3)
    res['response_code'] = 0
    print(res['msglist'])
    return json.dumps(res)


@app.route('/room/create_room', methods=['POST'])
@fl.login_required
def new_room():
    data = request.get_json()
    res = dict()
    enter = dict()
    prefix = '[G]'
    data['roomname'] = prefix + data['roomname']
    data['room_name'] = data.pop('roomname')
    enter['room_name'] = data['room_name']
    enter['account'] = fl.current_user.username
    flag = create_chatroom(data, db)
    if flag == 'success':
        res['response_code'] = 0
        enter_chatroom(enter, db)
        msg = dict()
        msg['account'] = fl.current_user.username
        msg['room_name'] = data['room_name']
        msg['message'] = 'Welcome to my chatroom!'
        send_message(msg, db)

    elif flag == 'duplicate':
        res['response_code'] = 1

    else:
        res['response_code'] = 2

    return json.dumps(res)


@app.route('/room/create_chat', methods=['POST'])
@fl.login_required
def new_chat():
    data = request.get_json()
    res = dict()
    prefix = '[P]'
    data['roomname'] = prefix + data['roomname']
    data['room_name'] = data.pop('roomname')
    other = data['othername']
    enter_me = dict()
    enter_other = dict()
    enter_me['account'] = fl.current_user.username
    enter_other['account'] = other
    enter_me['room_name'] = data['room_name']
    enter_other['room_name'] = data['room_name']
    flag = create_chatroom(data, db)

    if flag == 'success':
        res['response_code'] = 0
        enter_chatroom(enter_me, db)
        enter_chatroom(enter_other, db)
        msg = dict()
        msg['account'] = fl.current_user.username
        msg['room_name'] = data['room_name']
        msg['message'] = 'Nice to meet you!'
        send_message(msg, db)

    elif flag == 'duplicate':
        res['response_code'] = 1

    else:
        res['response_code'] = 2

    return json.dumps(res)


@app.route('/user/roomlist', methods=['POST', 'GET'])
@fl.login_required
def recent_room():
    if request.method == 'POST':
        db4 = pymysql.connect(**config)
        res = dict()
        data = request.get_json()
        usrname = data['username']
        print(usrname)
        lst = get_room_by_name(usrname, db4)
        print(lst)
        lst = [[a, b] for (a, b) in lst]
        for ls in lst:
            ls[1] = str(ls[1])
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
        data['account'] = data.pop('username')
        flag = change_pwd(data, db)
        if flag == 'success':
            res['response_code'] = 0
        elif flag == 'Wrong password':
            res['response_code'] = 1
        return json.dumps(res)


@app.route('/search', methods=['POST', 'GET'])
@fl.login_required
def room_search():
    if request.method == 'GET':
        return render_template('find.html')
    elif request.method == 'POST':
        db5 = pymysql.connect(**config)
        res = dict()
        data = request.get_json()
        typ = data['type']
        keyword = data['keyword']
        prefix = '[G]'
        res['response_code'] = 1
        if typ == 'room':
            res['roomlist'] = find_room(prefix + keyword, db5)
            res['response_code'] = 0
        else:
            res['userlist'] = find_name(keyword, db5)
            res['response_code'] = 0

        return json.dumps(res)


@app.route('/room/myroom', methods=['GET'])
@fl.login_required
def my_room():
    if request.method == 'GET':
        usrname = fl.current_user.username
        lsts = get_room_by_name(usrname, db)
        rooms = []
        for i in range(len(lsts)):
            lst = lsts[i]
            roomname = lst[0]
            if roomname[0:3] == '[G]':
                rooms.append(roomname)
        return render_template('chatroom.html', roomlist=rooms)


@app.route('/room/newroom', methods=['GET', 'POST'])
@fl.login_required
def new_room1():
    if request.method == 'GET':
        return render_template('new.html')


@app.route('/room/leave', methods=['POST'])
@fl.login_required
def leave_room():
    data = request.get_json()
    data['account'] = data.pop('username')
    data['room_name'] = data.pop('roomname')
    res = dict()
    res['response_code'] = 1
    flag = exit_chatroom(data, db)
    if flag == 'success':
        res['response_code'] = 0
    return json.dumps(res)


@app.route('/room/join', methods=['POST'])
@fl.login_required
def join_room():
    data = request.get_json()
    data['account'] = fl.current_user.username
    data['room_name'] = data.pop('roomname')
    flag = enter_chatroom(data, db)
    print(data)
    res = dict()
    res['response_code'] = 2
    if flag == 'success':
        res['response_code'] = 0
    elif flag == 'duplicate':
        res['response_code'] = 1
    return json.dumps(res)


@app.route('/user/send', methods=['POST'])
@fl.login_required
def send_msg():
    data = request.get_json()
    data['account'] = data.pop('username')
    data['message'] = data.pop('msg')
    data['room_name'] = data.pop('roomname')
    print(data)
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

