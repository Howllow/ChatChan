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

client needs to send a dict to server 

~~~ python
{
    'username':string
    'password':string
    'type':string
    'grpname':string
    'chatwith':string
    'message':string
}
~~~

* 'type' means the operation type:

  * register

  * login
  * makegrp
  * disgrp
  * entergrp
  * leavegrp
  * grpchat
  * prchat
  * grpmember
  * useronline
  * logout

* 'grpname'

  name of the group you're willing to make/enter/leave/dissolve

* 'chatwith'

  used in private chat, means who you want to chat with

* 'message'

  message you send while chatting



### Server

