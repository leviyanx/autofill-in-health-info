# Automatically fill in health info (yzu)

（2022-11-12）明天就是行程卡正式下线的日子，疫情封控的时代即将落幕，这个项目也到了归档的时刻了。

<img src="./images/IMG_3936.JPG"  height = "500" align=center />

## Requirement

1.python@3.10

2.python packages

```shell
pip3 install selenium webdriver_manager json smtplib email
```

3.user-info.json

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

explain location string : #TODO

4.manager_email_info.json

```json
{
  "from_address": "sender@mail.com",
  "from_address_pwd": "sender_password",
  "to_address": "receiver@mail.com"
}
```

5.crontab

## Run

Manual Execution

```shell
# 1. cd the script dir
# 2. execute this script
/usr/local/bin/python3.10 ./autofill.py
```

Timed Execution

1. set crontab task: `crontab -e`
2. fill these statements

```shell
# automatically fill health info in EVERYDAY 14:30
30 14 * * * bash /dir/to/autofill-health-info/autofill.sh >> /dir/to/autofill-health-info/crond-execution.log 2>&1 &
```

## Features

- [x] Locally, auto login, auto fill, auto submit
- [x] Recognize if the user has submitted the info
- [x] Remotely, perform above actions
- [x] fill for multiply users
- [x] If fail, logging related error, skip current user and not affect next user, notify manager.

## LICENCE

The MIT License (MIT)
