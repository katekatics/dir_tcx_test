import pymongo
from datetime import datetime, timedelta
import pandas as pd

def move():
    log_file = (pd.read_csv('logs/activity.csv')).values
    all_logs = []
    for i in log_file:
        log_list = i[0].split(';')
        logs = {}
        logs['date'] = datetime.strptime(log_list[0] + ' ' + log_list[1], '%Y-%m-%d %H:%M:%S') - timedelta(hours=3)
        logs['user'] = log_list[2]
        logs['action'] = log_list[3]
        if len(log_list) == 5:
            logs['sap'] = log_list[4]
        else:
            logs['sap'] = ''
        if len(log_list) == 6:
            logs['block'] = log_list[5]
        else:
            logs['block'] = ''
        all_logs.append(logs)
    return all_logs

def mongo():
    data = move()
    mongo = pymongo.MongoClient('192.168.200.73', 27017)
    db = mongo['tcx']
    col = db['logs']
    col.insert_many(data)
    mongo.close()

move()
mongo()

