# -*- coding:utf-8 _*-
""" 
@author:limuyu
@file: test.py.py 
@time: 2018/12/30
@contact: limuyu0110@pku.edu.cn

"""
from faker import Faker, Factory
import random
import json
import os
import time

from db.mydb import *
from db.config import *


def generating_users(conn):
    name_list = [
        'jinqingzhe',
        'chenzhengyin',
        'xiejinhan',
        'limuyu'
    ]
    for name in name_list:
        print(register_user({
            'account': name,
            'password': name,
        }, conn))

    return


def generating_chatrooms(conn):
    name_list = [
        'naruto',
        'one-piece',
        'durarara',
        'trump'
    ]
    for name in name_list:
        print(create_chatroom({
            'room_name': name
        }, conn))

    return


def generating_enters(conn):
    name_list = [
        'jinqingzhe',
        'chenzhengyin',
        'xiejinhan',
        'limuyu'
    ]
    for name in name_list:
        print(enter_chatroom({
            'account': name,
            'room_name': 'naruto',
        }, conn))

    return


def generating_messages(conn):
    name_list = [
        'jinqingzhe',
        'chenzhengyin',
        'xiejinhan',
        'limuyu'
    ]
    room_name = 'naruto'

    fake = Faker('zh-CN')
    for i in range(1000):
        name = random.sample(name_list, 1)[0]
        fake_message = fake.text(max_nb_chars=100)

        send_message({
            'account': name,
            'room_name': room_name,
            'message': fake_message
        }, conn)

    return


def entropy_naive(conn):
    room_list = [
        'one-piece',
        'durarara',
        'trump'
    ]
    fake = Factory.create()
    fake_zh = Faker('zh-CN')
    account_list = []
    for i in range(20):
        account = fake.user_name()
        account_list.append({'account': account})
        register_user({
            'account': account,
            'password': account
        }, conn)

    for item in account_list:
        # entering random number of rooms
        get_into_these_rooms = random.sample(room_list, random.randint(1, 3))
        item['room_names'] = get_into_these_rooms

        for room in get_into_these_rooms:
            enter_chatroom({
                'account': item['account'],
                'room_name': room
            }, conn)

    for i in range(200):
        item = random.sample(account_list, 1)[0]
        account = item['account']
        room_name = random.sample(item['room_names'], 1)[0]
        message = fake_zh.text(max_nb_chars=100)

        send_message({
            'account': account,
            'room_name': room_name,
            'message': message
        }, conn)


if __name__ == '__main__':
    connection = pymysql.connect(**config)
    # generating_users(connection)
    # generating_chatrooms(connection)
    # generating_enters(connection)
    # print('-' * 70)
    # print(json.dumps(get_messages_from_room_name({'room_name': 'naruto'}, connection), ensure_ascii=False, indent=4))
    # print('-' * 70)

    # print(json.dumps(get_members_from_room_name({'room_name': 'naruto'}, connection), ensure_ascii=False, indent=4))
    # exit_chatroom({'account': 'limuyu', 'room_name': 'naruto'}, connection)
    # print(json.dumps(get_members_from_room_name({'room_name': 'naruto'}, connection), ensure_ascii=False, indent=4))

    register_user({
        'account': 'limuyu',
        'password': 'limuyu'
    }, connection)

    # login_user({
    #     'account': 'lmuyu',
    #     'password': '123',
    # }, connection)
    # entropy_naive(connection)
