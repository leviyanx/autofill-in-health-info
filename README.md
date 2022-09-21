yzu auto fill health info script

Requirement

python@3.10

```shell
pip3 install selenium webdriver_manager
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

Features

Locally, auto login, auto fill, auto submit
Remotely, perform above actions (in specified time)
fill for multiply users
if fail, notify manager