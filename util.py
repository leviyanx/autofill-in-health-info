import json


def load_json_data(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data


def notify_manager():
    print("notify")

