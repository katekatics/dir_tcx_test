import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import xlsxwriter
from datetime import datetime
import pymongo
import os

def get_data(start_date, end_date):
    """Создание словаря на основе данных из лога, в словаре содержится количество кликов и количество скачанных отчетов в дашборде для директоров."""
    conn = pymongo.MongoClient('192.168.200.73',27017)
    db = conn['tcx']
    coll = db.logs
    sp=[]
    cursor=coll.find({'date':{'$lt': end_date,'$gte': start_date}})
    for i in cursor:
        sp.append([i['block'],i['action']])
    conn.close()

    clicks = {
        'business_revenue_new_body': 0,
        'business_rto_body': 0,
        'business_average_check_body': 0,
        'business_canceled_checks_body': 0,
        'business_write_offs_body': 0,
        'business_sellers_perfom_body': 0,
        'business_open_documents_body': 0,     
        'markdown_body': 0,
        'products_overdue_body': 0, 
        'products_low_saled_body': 0, 
        'products_minus_body': 0,
        'products_top30_body': 0, 
        'products_topvd_body': 0, 
        'products_stoped_body': 0, 
        'products_stoped_fresh_body': 0, 
        'products_stoped_food_body': 0,   
        'business_checks_traffic_body': 0, 
        'business_old_price_body': 0,
        'hr_indicators_body': 0,
        'products_super_price_body': 0
    }
    reports = {
        'business_revenue_new_report': 0,
        'business_rto_report': 0,
        'business_average_check_report': 0,
        'business_canceled_checks_report': 0,
        'business_write_offs_report': 0,
        'business_sellers_perfom_week_report': 0,
        'business_sellers_perfom_month_report': 0,
        'business_sellers_perfom_report': 0,
        'business_open_documents_report': 0,
        'markdown_report': 0,
        'products_overdue_report': 0, 
        'products_low_saled_report': 0, 
        'products_minus_report': 0,
        'products_top30_report': 0, 
        'products_topvd_report': 0, 
        'products_stoped_report': 0, 
        'products_stoped_fresh_report': 0, 
        'products_stoped_food_report': 0,   
        'business_checks_traffic_report': 0, 
        'business_old_price_report': 0,
        'hr_indicators_report': 0,
        'products_super_price_report': 0
    }
    data = {'clicks': clicks, 'reports': reports}#создаем словарь словарей
    for i in sp:
        if i[1] == 'click':
            if i[0] in clicks:
                clicks[i[0]] += 1
        try:
            if i[1].endswith('report'):
                reports[i[1]] += 1
        except:
            continue
    
    return data

def build_excel(start_date, end_date):
    """Создание ексель файла, листа в нем, а также столбцов и строк"""
    data = get_data(start_date, end_date)
    names = {#Наименование блоков на русском языке
        'business_revenue_new': 'Продажи',
        'RTO': 'РТО',
        'business_average_check': 'Средний чек',
        'business_canceled_checks': 'Отмененные чеки',
        'business_write_offs': 'Списания',
        'business_sellers_perfom': 'Производительность кассиров',
        'business_open_documents': 'Открытые документы приемки',
        
        'markdown': 'Markdown',
        'products_overdue': 'Просроченная продукция',
        
        'products_low_saled': 'Низкие продажи',
        'products_top30': 'Топ 30',
        'products_topvd': 'Топ ВД',
        'products_stoped_food': 'Товары без движения FOOD + NONFOOD',
        'products_stoped_fresh': 'Товары без движения FRESH',
        'products_minus': 'Товары с отрицательными остатками',
        'business_checks_traffic': 'Трафик чеков',
        'business_old_price': 'Продажи по старой цене',
        'products_super_price': 'Суперцена'
    }
    workbook = xlsxwriter.Workbook('media/heatmap.xlsx')#Создаем xlsx файл для тепловой карты
    worksheet = workbook.add_worksheet()#Добавляем в файле лист
    row = 0
    col = 0

    worksheet.write(row, col, 'block')#Создаём имя первого столбца(имя блока на нашем сайте)
    worksheet.write(row, col+1, 'action')#Второго столбца(дейтсвие которое было совершено, скачиваение отчёта или клик)
    worksheet.write(row, col+2, 'count')#Число действий
    for key in names.keys():
        row += 1
        worksheet.write(row, col, names[key])
        worksheet.write(row, col+1, 'Клик по блоку')
        if (key + '_body') in data['clicks']:
           worksheet.write(row, col+2, data['clicks'][key + '_body'])#сколько было кликов по этому блоку
        else:
            worksheet.write(row, col+2, 0)#иначе ничего не прибавляем
        row += 1
        worksheet.write(row, col, names[key])
        worksheet.write(row, col+1, 'Скачивание отчета')
        if (key + '_report') in data['reports']:
            worksheet.write(row, col+2, data['reports'][key + '_report'])#сколько раз скачали отчет
        else:
            worksheet.write(row, col+2, 0) #иначе ничего не прибавляем
    workbook.close()

def build_heatmap(start_date, end_date):
    """Создание тепловой карты"""

    build_excel(start_date, end_date)
    action_raw = pd.read_excel('media/heatmap.xlsx')  
    action_matrix = action_raw.pivot( 'block', 'action','count')  
    fig, axes = plt.subplots(figsize=(6,9)) # (Ширина, высота)
    axes.tick_params(axis="x", labelsize=8)
    axes.tick_params(axis="y", labelsize=10)
    sns.heatmap(action_matrix, ax = axes, annot=True, square=True, cmap='PuBu', fmt='d', linewidths=.5)
    start = datetime.strftime(start_date, '%Y-%m-%d %H:%M:%S')
    end = datetime.strftime(end_date, '%Y-%m-%d %H:%M:%S')
    file_start = datetime.strftime(start_date, '%Y-%m-%d_%H-%M-%S')
    file_end = datetime.strftime(end_date, '%Y-%m-%d_%H-%M-%S')
    axes.set_title('Тепловая карта за период' + '\n' + start + ' - ' + end, pad=10)
    axes.xaxis.labelpad=40   
    axes.xaxis.set_tick_params(rotation=50)
    
    if not os.path.exists('media/heatmap'):
        os.makedirs('media/heatmap')
    fig.savefig('media/heatmap/heatmap_' + file_start + '_' + file_end + '.png')
