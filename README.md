# ChatChan(Updated Dec/03)
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

### Server

