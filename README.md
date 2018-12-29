# ChatChan(Updated Dec/29)
a naive online chat program(python)



### Functions to be implemented

* Registration
* Login
* Make a group
* Dissolve a group
* Enter a group
* Leave a group
* Chat in the group
* Chat privately
* See group member
* See online users
* Logout



### API

* Get recent chatroom

operation：room/recent

method: post

send: 

```
userid: number
```

response:

```
response_code: number
roomlist: list
```

* Get chatroom message list

operation: room/msg

method: post

send:

```
roomid: number
```

response:

```
response_code: number
msg_list: list
```

* Get chatroom list

operation: user/roomlist

method: post

send:

```
userid: number
type: number(0 for created room/1 for joined room)
```

response:

```
response_code: number
roomlist: list
```

* Create a chatroom

operation: room/new

method: post

send:

```
roomname: string
room_ownerid: number
description: string
```

response:

```
response_code: number
roomid: number
```

* Search for chatroom

operation: room/search

method: post

send:

```
keyword: string
```

response:

```
response_code: number
roomlist: list
```

* Change user profile

operation: user/profile

method: post

send:

```
gender: number
(others)
```

response:

```
response_code: number
```

* Change password

operation: user/setting

method: post

send:

```
username: string
old_password: string
new_password: string
```

response:

```
response_code: number
```

* login

operation: login

method: post

send:

```
username: string
password: string
```

response:

```
response_code: number
```

* register

operation: register

method: post

send:

```
username: string
password: string
```

response:

```
response_code: number
```

* logout

depends on user management?

### Database Functions（mydb.py）

* check_reglog(json)

  * input:
    ~~~ 
    username:string
    password:string
    opcode:0(login)/register(1)
    ~~~

  * function: 
    - check if username has existed(login)
    - check if user is existed, then check the password(register)

  * output: 

    ~~~
    response_code:0(failed)/1
    ~~~

* create_room(json)

  * input:
    ~~~ 
    roomname:string
    room_owner:string
    description:string
    ~~~

  * function:
    * check if room has existed, if not, create it and record the room info

  * output: 

    ~~~
    response_code:0/1
    ~~~

* room_lst(json)

  * input:

    ~~~ 
    username:string
    type:0/1
    ~~~

  * function:

    * opcode = 1: return the rooms user is in
    * opcode = 0: only return the rooms user created

  * output:

    ~~~
    response_code:0/1
    roomlist:list
    ~~~
* search_room(json)
  * input:
    ~~~
    key_word:string
    ~~~
  * function:
    * find chatrooms using the given keyword
  * output:
    ~~~
    response_code:0/1
    roomlist:list
    ~~~
 
* change_pwd(json)

  * input:

    ~~~
    username:string
    old_password:string
    new_password:string
    ~~~

  * function:

    * check if old_password is correct
    * then change it

  * output:

    ~~~
    response_code:0/1
    ~~~

* msg_lst(json)

  * input:

    ~~~ 
    roomname:string
    ~~~

  * function:

    * return all messages in this room
    * meanwhile update "message_num" in all rooms, and see if there are changes

  * output:

    ~~~
    response_code:0/1
    msg_list:list
    change_list:list(contents are (roomname, newmsg_num))
    ~~~
* change_profile(json)
  * input:
    ~~~
    username:string
    category:string(e.g. gender)
    value:string
    ~~~
  * function:
    * change user's profile.
  * output:
    ~~~
    response_code:0/1
    ~~~

  ​