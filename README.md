# Automatically fill in health info (yzu)

2022-12-12：明天就是行程卡正式下线的日子，疫情封控的时代即将落幕，这个项目也到了归档的时刻了。（2019.12～2022.12）

<img src="./images/IMG_3936.JPG"  height = "500" align=center />

## Requirement

Environment: Python@3.10

Denpendences. Install these python packages:

```shell
pip3 install selenium webdriver_manager json smtplib email
```

Create a `user-info.json` in project root directory, the contents in the file like this, and fill in information of user who want to use this script.

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

Tip: Now `location` item don't need to be filled in, and you should leave it without any action.

Create a `manager_email_info.json` file in root directory of project, and the content in it like this. Replace these information with yours.

```json
{
  "from_address": "sender@mail.com",
  "from_address_pwd": "sender_password",
  "to_address": "receiver@mail.com"
}
```

## Usage

### Manual Execution

```shell
# 1. cd the script dir
# 2. execute this script
/usr/local/bin/python3.10 ./autofill.py
```

### Scheduled execution

1. Set crontab task: `crontab -e`
2. Fill in these expression:

```shell
# automatically filling in health info in EVERYDAY 14:30
30 14 * * * bash /dir/to/autofill-health-info/autofill.sh >> /dir/to/autofill-health-info/crond-execution.log 2>&1 &
```

## Features

- [x] In local machine, auto login, auto fill, auto submit
- [x] Identify whether the user has submitted the information
- [x] In server, perform above actions
- [x] Support multiple users
- [x] If fail, logging related error, skip current user and not affect next user, notify manager.

## LICENCE

The MIT License (MIT)
