# -*- coding:utf-8 _*-
""" 
@author:limuyu
@file: mydb.py 
@time: 2018/12/30
@contact: limuyu0110@pku.edu.cn

"""
import pymysql
from pymysql.connections import Connection
from typing import Dict
import datetime
from db.utils import check

from db.config import *


def register_user(data: Dict[str, str], conn: Connection):
    """

    :param data:
        python dictionary, containing keys as follows:
            account: string (len < 20)
            password: string (len < 20)
    :param conn:
        pymysql connection
    :return:
        message:
            success: registering succeeded
            duplicate: account name already exists
            failed: some other errors (probably wrong keys)

    """
    if not check(['account', 'password'], data, 'register'):
        return 'failed'

    cursor = conn.cursor()

    ### checking duplicates in a very stupid method...
    sql = 'select account from user;'
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        if data['account'] == row:
            logging.debug(F'user account {data["account"]} already exists')
            return 'duplicate'
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = F"insert into user (account, password, register_date)" \
        F" VALUE ('{data['account']}', '{data['password']}', '{dt}');"
    cursor.execute(sql)

    conn.commit()
    cursor.close()

    logging.debug(F'register for account {data["account"]} succeeded')
    return 'success'


def create_chatroom(data: Dict[str, str], conn: Connection):
    """
    :param data:
        python dictionary, containing keys as follows:
            room_name: string (len < 20)
            password: string (len < 20)
    :param conn:
        pymysql connection
    :return:
        message:
            success: creation succeeded
            duplicate: room name already exists
            failed: some other errors (probably wrong keys)
    """

    if not check(['room_name'], data, 'register'):
        return 'failed'
    if 'password' not in data:
        data['password'] = ''

    cursor = conn.cursor()

    ### checking duplicates in a very stupid method...
    sql = 'select room_name from chat_room;'
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        if data['room_name'] == row:
            logging.debug(F'room {data["room_name"]} already exists')
            return 'duplicate'

    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = F"insert into chat_room (room_name, password, create_time)" \
        F" VALUE ('{data['room_name']}', '{data['password']}', '{dt}');"
    cursor.execute(sql)

    conn.commit()
    cursor.close()

    logging.debug(F'creating room: {data["room_name"]} succeeded')
    return 'success'


def enter_chatroom(data: Dict[str, str], conn: Connection):
    """

    :param data:
        python dictionary, containing keys as follows:
            account: string (len < 20)
            room_name: string (len < 20)
    :param conn:
        pymysql connection
    :return:
        message:
            success: entering succeeded
            failed: some other errors

    """

    cursor = conn.cursor()
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = F"insert into chatting(account, room_name, enter_time, if_active) " \
        F"value ('{data['account']}', '{data['room_name']}', '{dt}', 1)"

    cursor.execute(sql)
    conn.commit()
    cursor.close()

    logging.debug(F'account : {data["account"]} entering {data["room_name"]}')
    return 'success'


def exit_chatroom(data: Dict[str, str], conn: Connection):
    """

    :param data:
        python dictionary, containing keys as follows:
            account: string (len < 20)
            room_name: string (len < 20)
    :param conn:
        pymysql connection
    :return:
        message:
            success: exiting succeeded
            failed: some other errors

    """

    cursor = conn.cursor()

    sql = F"update chatting set if_active=0 where room_name = '{data['room_name']}' and account = '{data['account']}'"

    cursor.execute(sql)
    conn.commit()
    cursor.close()

    logging.debug(F'account : {data["account"]} exiting {data["room_name"]}')
    return 'success'


def send_message(data: Dict[str, str], conn: Connection):
    """

    :param data:
    :param conn:
    :return:
    """
    cursor = conn.cursor()
    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sql = F"insert into messages(account, room_name, message, send_time) " \
        F"value('{data['account']}', '{data['room_name']}', '{data['message']}', '{dt}')"

    cursor.execute(sql)
    conn.commit()

    cursor.close()

    logging.debug(F'account : {data["account"]} sending message in room : {data["room_name"]}')
    return 'success'


def get_messages_from_room_name(data: Dict[str, str], conn: Connection):
    cursor = conn.cursor()

    sql = F"select account, message, send_time\
            from messages\
            where room_name = '{data['room_name']}'"

    cursor.execute(sql)
    cursor.close()
    messages = cursor.fetchall()

    n = data['n_messages'] if 'n_messages' in data else 100

    messages = [
        {
            'account': a[0],
            'message': a[1],
            'time': str(a[2])
        }
        for a in sorted(messages, key=lambda x: x[2])[:n]
    ]

    return messages


def get_members_from_room_name(data: Dict[str, str], conn: Connection):
    cursor = conn.cursor()

    sql = F"select account from chatting where room_name = '{data['room_name']}' and if_active = 1"

    cursor.execute(sql)
    users = cursor.fetchall()

    cursor.close()

    return [a[0] for a in users]


def get_all_room_names(conn: Connection):
    """

    :param conn:
    :return:
        list of all rooms
    """
    cursor = conn.cursor()

    sql = F"select room_name from chat_room"

    cursor.execute(sql)
    rooms = cursor.fetchall()

    cursor.close()

    return [a[0] for a in rooms]
