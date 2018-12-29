from flask import *
from flask_socketio import *
from mydb import *
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chatchan'


@app.route('/')
def homepage():
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        data['opcode'] = 1
        return check_reglog(data)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        data['opcode'] = 0
        return check_reglog(data)


@app.route('/room/msg', methods=['GET'])
def get_msg():
    data = request.get_json()
    return msg_lst(data)


@app.route('/room/new', methods=['POST'])
def new_room():
    data = request.get_json()
    return create_room(data)


@app.route('/user/roomlist', methods=['POST', 'GET'])
def recent_room():
    if request.method == 'POST':
        data = request.get_json()
        return room_lst(data)


@app.route('/user/setting', methods=['POST', 'GET'])
def usr_set():
    if request.method == 'GET':
        return render_template('setting.html')
    elif request.method == 'POST':
        data = request.get_json()
        return change_pwd(data)


@app.route('/user/profile', methods=['POST', 'GET'])
def usr_info():
    if request.method == 'GET':
        return render_template('info.html')
    elif request.method == 'POST':
        data = request.get_json()
        return change_profile(data)


@app.route('/room/search', methods=['POST', 'GET'])
def room_search():
    if request.method == 'GET':
        return render_template('find.html')
    elif request.method == 'POST':
        data = request.get_json()
        return search_room(data)


if __name__ == '__main__':
    app.run(host='localhost', port='5000')

