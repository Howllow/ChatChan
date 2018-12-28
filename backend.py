from flask import *
import json

app = Flask(__name__)
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
        'do some database operation here'
        print(username)
        return json.dumps({'response_code':1})

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        'do some db'
        return json.dumps({'response_code': 1})

if __name__ == '__main__':
    app.run(host='localhost', port='5000', debug=True)


