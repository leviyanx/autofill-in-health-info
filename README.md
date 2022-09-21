yzu auto fill health info script

Requirement

python@3.10

```shell
pip3 install selenium webdriver_manager json smtplib email
```

user-info.json

```json
{
  "users_info": [
    {
      "username": "u1",
      "password": "p1",
      "in_campus_status": "True",
      "location": ""
    },
    {
      "username": "u2",
      "password": "p2",
      "in_campus_status": "True",
      "location": ""
    }
  ]
}
```

explain location string : TODO

manager_email_info.json

```json
{
  "from_address": "sender@mail.com",
  "from_address_pwd": "sender_password",
  "to_address": "receiver@mail.com"
}
```

Features

️-[x] Locally, auto login, auto fill, auto submit
-[] Remotely, perform above actions (in specified time)
-[x] fill for multiply users
-[] If fail, log related error, skip current user and not affect next user, notify manager.
