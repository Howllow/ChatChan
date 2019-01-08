import flask_login as fl

class User(fl.UserMixin):
    def __init__(self):
        self.username = None
        self.id = None
    def __repr__(self):
        return '<User %r>' % self.username

class UserManager:
    def __init__(self):
        pass

    @classmethod
    def get(self, id):
        user = User()
        user.username = id
        user.id = id
        return user
