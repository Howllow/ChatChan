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
        reg_message = register_user(data, db)
        if reg_message == 'success':
            return redirect(url_for('login'))
        else:
            return render_template('register.html', message=reg_message)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()
        data['account'] = data.pop('username')
        log_message = login_user(data, db)
        if log_message == 'success':
            usr = user.User()
            usr.username = data['account']
            fl.login_user(usr)
            flash('Login Success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        else:
            return render_template('login.html', message=log_message)


@app.route('/home', methods=['GET', 'POST'])
@fl.login_required
def home():
    if request.method == 'GET':
        return render_template('home.html')


@app.route('/room/msg', methods=['GET'])
@fl.login_required
def get_msg():
    data = request.get_json()
    return msg_lst(data)


@app.route('/room/new', methods=['POST'])
@fl.login_required
def new_room():
    data = json.loads(request.get_json())
    return create_room(data)


@app.route('/user/roomlist', methods=['POST', 'GET'])
@fl.login_required
def recent_room():
    if request.method == 'POST':
        data = request.get_json()
        return room_lst(data)


@app.route('/user/setting', methods=['POST', 'GET'])
@fl.login_required
def usr_set():
    if request.method == 'GET':
        return render_template('setting.html')
    elif request.method == 'POST':
        data = request.get_json()
        return change_pwd(data)


@app.route('/user/profile', methods=['POST', 'GET'])
@fl.login_required
def usr_info():
    if request.method == 'GET':
        return render_template('info.html')
    elif request.method == 'POST':
        data = request.get_json()
        return change_profile(data)


@app.route('/room/search', methods=['POST', 'GET'])
@fl.login_required
def room_search():
    if request.method == 'GET':
        return render_template('find.html')
    elif request.method == 'POST':
        data = request.get_json()
        return search_room(data)


if __name__ == '__main__':
    app.run(host='localhost', port='5000')

