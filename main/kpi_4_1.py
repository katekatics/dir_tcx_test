import pandas as pd 
from datetime import timedelta, datetime, date, time
import pymongo
import matplotlib.pyplot as plt
import os
import xlsxwriter
from itertools import groupby

def get_user(start_date, end_date):
    """Получение уникальных юзеров из MongoDb за промежуток времени start_date - end_date.
    Возвращаемое значение: список уникальных юзеров."""
    conn = pymongo.MongoClient('192.168.200.73',27017)
    db = conn['tcx']
    coll = db.logs
    sp=[]
    cursor=coll.find({'date':{'$lt':end_date,'$gte':start_date}})
    for i in cursor:
        sp.append(i["user"])
    conn.close()
    sp.sort()
    new_sp = [el for el, _ in groupby(sp)]
    return new_sp


def count_market():
    """Подсчёт количества всех магазинов"""
    conn = pymongo.MongoClient('192.168.200.73',27017)
    db = conn['tcx']
    coll = db.stores
    all_markt=[]
    curs=coll.find({})
    for i in curs:
        all_markt.append(i["_id"])
    conn.close()
    n=len(all_markt)
    return n


def get_user_and_date(start_date, end_date):
    us=[]
    conn = pymongo.MongoClient('192.168.200.73',27017)
    db = conn['tcx']
    coll = db.logs
    sp=[]
    cursor=coll.find({'date':{'$lt':end_date,'$gte':start_date}})
    for i in cursor:
        sp.append([i["user"],i["date"]])
    conn.close()
  
    return sp


def create_kpi_graph(dirs, start_date, end_date):
    par=5
    users_and_date=get_user_and_date(start_date, end_date)


    df = pd.DataFrame(users_and_date, columns=['user','date'])
    df["clean_data"] = df["date"].dt.date
    grouped_on_dt_and_user = df.groupby(['user','clean_data'])['date'].count().reset_index()
    all_users = grouped_on_dt_and_user.groupby('clean_data')['user'].count().reset_index()
    grouped_on_dt_and_user['is_active'] = grouped_on_dt_and_user['date'].apply(lambda x:x>=par)
    active_users = grouped_on_dt_and_user.groupby('clean_data')['is_active'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(13,8))
    ax.plot(all_users['clean_data'],all_users['user'],label="Все пользователи")
    ax.plot(active_users['clean_data'],active_users['is_active'], label='Активные пользователи' + '\n' + '(клики более '+str(par)+')')
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,fontsize=16)
    plt.legend(fontsize=10)
    ax.set_title('KPI', pad=10)
    file_start = datetime.strftime(start_date, '%Y-%m-%d_%H-%M-%S')
    file_end = datetime.strftime(end_date, '%Y-%m-%d_%H-%M-%S')
    if not os.path.exists('media/kpi'):
        os.makedirs('media/kpi')
    fig.savefig('media/kpi/kpi_' + file_start + '_' + file_end + '.png')
    t_all='all_'
    t_ac='active_'
    download_excel(all_users,start_date, end_date,t_all)
    download_excel(active_users,start_date, end_date,t_ac)
    kpi_report(dirs, start_date, end_date)

    
def download_excel(users,start_date, end_date, tp):
    s_d = datetime.strftime(start_date, '%Y-%m-%d_%H-%M-%S')
    e_d = datetime.strftime(end_date, '%Y-%m-%d_%H-%M-%S')
    users.to_excel(os.getcwd()+'/media/report_'+ tp + s_d + '_' + e_d + '.xlsx', sheet_name='Sheet1')



def kpi_report(dirs, start_date, end_date):
    user = get_user(start_date,end_date)
    directors=[]
    for i in user:
        if i in dirs:
            directors.append(i)
    WAU = len(directors) 
    all_user = count_market()
    activation_rate = round(((WAU / all_user)*100),2)
    users_and_date=get_user_and_date(start_date, end_date)
    dirs_and_date=[]
    for i in users_and_date:
        if i[0] in dirs:
            dirs_and_date.append(i)
    df = pd.DataFrame(dirs_and_date, columns=['user','date'])
    df["clean_data"] = df["date"].dt.date
    grouped_on_dt_and_user = df.groupby(['user','clean_data'])['date'].count().reset_index()
    all_users = grouped_on_dt_and_user.groupby('clean_data')['user'].count().reset_index()
    DAU = round(all_users['user'].mean())
    stickiness = round(((DAU / WAU)*100),2)
    
    file_start = datetime.strftime(start_date, '%Y-%m-%d_%H-%M-%S')
    file_end = datetime.strftime(end_date, '%Y-%m-%d_%H-%M-%S')
    workbook = xlsxwriter.Workbook(os.getcwd()+'/media/kpi_report_' + file_start + '_' + file_end + '.xlsx')
    worksheet = workbook.add_worksheet()#Добавляем в файле лист
    row = 0
    col = 0
    worksheet.write(0,0,'Activation ratу')
    worksheet.write(0,1,'DAU')
    worksheet.write(0,2,'WAU')
    worksheet.write(0,3,'Stickiness')
    worksheet.write(1,0,activation_rate)
    worksheet.write(1,1,DAU)
    worksheet.write(1,2,WAU)
    worksheet.write(1,3,stickiness)
    worksheet.write(5,0,'Отчёт собран за даты:')
    worksheet.write(4,1,'Начало периода')
    worksheet.write(4,2,'Конец периода')
    worksheet.write(5,1,file_start)
    worksheet.write(5,2,file_end)
    workbook.close()

