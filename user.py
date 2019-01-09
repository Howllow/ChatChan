# -*- coding:utf-8 _*-
"""
@author:howllow(jinqingzhe)
@file: user.py
@time: 2019/1/9
@contact: 1600012896@pku.edu.cn

"""
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
    def get(cls, i):
        user = User()
        user.username = i
        user.id = i
        return user
