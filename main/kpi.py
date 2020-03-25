import pandas as pd 
from datetime import timedelta, datetime, date, time
import pymongo
import matplotlib.pyplot as plt
import os
import xlsxwriter
from itertools import groupby
from pathlib import Path

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

def user_click_date(start_date, end_date):
    conn = pymongo.MongoClient('192.168.200.73',27017)
    db = conn['tcx']
    coll = db.logs
    sp = []

    cursor = coll.aggregate([
       { '$match': {'date':{'$lt':end_date,'$gte':start_date}}},
       { '$group': { '_id': "$user", 'count': { '$sum': 1 }, 'date' :  { '$push':  "$date"  }  } }
    ])

    for i in cursor:
        date_only=[]
        for j in i["date"]:
            date=str(j.day)+'-'+str(j.month)+'-'+str(j.year)
            date_only.append(date)
        
        sp.append([i["_id"], date_only, i["count"]])
    return sp

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
    """Создание графика по KPI"""
    par=5
    users_and_date=get_user_and_date(start_date, end_date)
    df = pd.DataFrame(users_and_date, columns=['user','date'])
    df["clean_data"] = df["date"].dt.date
    grouped_on_dt_and_user = df.groupby(['-','clean_data'])['date'].count().reset_index()
    all_users = grouped_on_dt_and_user.groupby('clean_data')['user'].count().reset_index()
    grouped_on_dt_and_user['is_active'] = grouped_on_dt_and_user['date'].apply(lambda x:x>=par)
    active_users = grouped_on_dt_and_user.groupby('clean_data')['is_active'].sum().reset_index()
    active_and_all_users = pd.merge(active_users,all_users,on='clean_data', how='inner')
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
    download_excel(active_and_all_users,start_date, end_date,t_all)
    # download_excel(active_users,start_date, end_date,t_ac)
    kpi_report(dirs, start_date, end_date)

    
def download_excel(users,start_date, end_date, tp):
    s_d = datetime.strftime(start_date, '%Y-%m-%d_%H-%M-%S')
    e_d = datetime.strftime(end_date, '%Y-%m-%d_%H-%M-%S')
    users.to_excel(os.getcwd()+'/media/report_'+ tp + s_d + '_' + e_d + '.xlsx', sheet_name='Sheet1')



def kpi_report(dirs, start_date, end_date):
    """Показатели по KPI"""
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



def get_base_dirs(directors_sql, start_date, end_date):
    """Подготовка данных"""
    logs_user = get_user(start_date, end_date)
    direct = os.path.dirname(os.path.abspath(__file__))
    direct_parent = str(Path(direct).parent)
    if os.listdir(path=direct_parent + '/media'):
        df = pd.read_excel(direct_parent + '/media/dir_and_sap.xlsx')
    dirs = []
    # рандж надо заменить на шейп
    for i in range(867):
        dirs.append(df.iloc[i].to_list())
    # приводим имена директоров и региональных директоров к общему виду, а также регионы,чтобы корректно в дальнейшем выполнить группировку.
    for i in range(len(dirs)):
        dirs[i][0]=str(dirs[i][0]).strip().lower()
        dirs[i][1]=str(dirs[i][1]).strip().lower()
        dirs[i][2]=str(dirs[i][2]).strip().lower()
        dirs[i][4]=str(dirs[i][4]).lower()
        
    sort_user=[]
    for i in logs_user:
        for j in dirs:
            if i == j[0]:
                sort_user.append(['D',i,'',j[2],j[3],j[4],j[5]])
                
            elif i == j[1]:
                sort_user.append(['RD',i,'','','',j[4],j[5]])
    us=[]
    for i in sort_user:
        us.append(i[1])
    # вычитаем директоров из всех логов, тчобы получить остальных пользователей. 
    set_dirs=set(us)
    set_all=set(logs_user)
    itog = set_all - set_dirs
    itog_list = list(itog)
    base=[]
    # директора из базы 
    for i in itog_list:
        for j in directors_sql:
            if i == j[1]:
                base.append(j)

    directors_sql_only_name = []
    [directors_sql_only_name.append(d[1]) for d in directors_sql]   
    set_directors_sql = set(directors_sql_only_name)
    who_did_not_use = list(set_directors_sql - set_all)
    

    base_sort=[]
    for i in base:
        for j in dirs:
            if str(i[0]).lower()==str(j[2]).lower():
                base_sort.append(['DL',i[1],j[0],j[2],j[3],j[4],j[5]])
    
    who_did_not_use_lst = []
    for i in who_did_not_use:
        for j in dirs:
            if i == j[0]:
                who_did_not_use_lst.append(['DN', i, None, j[2], j[3], j[4], j[5]])
                
    # делаем группировку, чтобы региональные директора не повторялись много раз.         
    sort_user.sort(key=lambda x:x[1])
    new_sort_user = [el for el, _ in groupby(sort_user)]
    for i in base_sort:
        new_sort_user.append(i)
    
    for i in who_did_not_use_lst:
        new_sort_user.append(i)

    
    return new_sort_user


def get_result_activity(dirs, start_date, end_date):
    """Создание сводной таблицы"""
    user_action = user_click_date(start_date, end_date)
    user_date_count = []
    s2_d = start_date
    for i in user_action:
        start_date = s2_d
        while (start_date < end_date):  
            col = 0      
            date = str(start_date.day)+'-'+str(start_date.month)+'-'+str(start_date.year)
            for j in i[1]:
                if j == date:
                    col+=1
            user_date_count.append([i[0],date,col])
            start_date += timedelta(days=1)

    df_count_date_user_nogroup = pd.DataFrame(user_date_count, columns=['user','date','click'])
    user_date_count_matrix = df_count_date_user_nogroup.pivot( 'user', 'date','click')  
    my_sorted_list = pd.to_datetime(user_date_count_matrix.columns, format='%d-%m-%Y').sort_values()
    my_sorted_list_str = my_sorted_list.day.astype(str) + '-' + my_sorted_list.month.astype(str) + '-' + my_sorted_list.year.astype(str)
    user_date_count_matrix = user_date_count_matrix[my_sorted_list_str]

    sort_base_users = get_base_dirs(dirs, s2_d, end_date)
    sort_base_users.sort(key=lambda x:x[3])

    dirs_bd = pd.DataFrame(sort_base_users, columns=['type','user','dir','sap','market','region','division'])
    activity = pd.merge(dirs_bd,user_date_count_matrix,on='user',how='outer')
    file_start = datetime.strftime(s2_d, '%Y-%m-%d_%H-%M-%S')
    file_end = datetime.strftime(end_date, '%Y-%m-%d_%H-%M-%S')
    activity.to_excel(os.getcwd()+'/media/activity_' + file_start + '_' + file_end + '.xlsx')
