import pymongo
from datetime import datetime
import dns
import os

password = os.getenv("password")
user = os.getenv("user")

client = pymongo.MongoClient(
    "mongodb+srv://userio:" + password +
    "@cluster.geizz.mongodb.net/?retryWrites=true&w=majority")

db = client.webhook
col = db.github


def store_data(data):
    col.insert_one(data)


def get_main():
    data = col.find({}, limit=20).sort('timestamp', -1)
    return data


def get_after_time(timestamp):
    data = col.find({
        "timestamp": {
            "$gt": datetime.fromisoformat(timestamp[:-1])
        }
    }).sort('timestamp', 1)
    return data


def format_data(datalist):
    action = {'PUSH': 'push', 'PULL_REQUEST': 'pull', 'MERGE': 'merge'}
    month = [
        'January', 'Febuary', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December'
    ]
    formatdata = []
    for data in datalist:
        data['_id'] = ""
        data['action'] = action[data['action']]
        ts = data['timestamp']
        data['timestamp'] = ts.strftime('%d {}, %Y %H:%M:%S'.format(
            month[ts.month - 1]))
        formatdata.append(data)
    return formatdata

