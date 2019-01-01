import flask_login as fl

class User(fl.UserMixin):
    def __init__(self):
        self.username = None

    def __repr__(self):
        return '<User %r>' % self.username

