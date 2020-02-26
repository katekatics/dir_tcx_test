from django.shortcuts import render, redirect
from . import store_class
from .models import Message, Incident, Dirs
from django.contrib.auth.decorators import login_required
from .ad import checkUserInAD, checkUserGroup
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm
from django.http import JsonResponse
from datetime import datetime, timedelta
import os
from django.http import HttpResponse, HttpResponseRedirect
import xlsxwriter
from django.core.files.storage import FileSystemStorage
import shutil
from django.contrib import messages
import pymongo
from cefevent import CEFEvent
from functools import wraps
import socket
from . import heatmap
from time import sleep
import json 
import calendar
import time, sys
from . import kpi_4_1
from . import account
import paramiko

# LOGGER
import logging
from logging.handlers import RotatingFileHandler

sprint = '_3_'
version = '1'

# with open(os.getcwd() + '/logs/dir_tcx.log', "w+") as f:
#     f.write(socket.gethostname())

dirs = Dirs.objects.all()
directors = []
dir_all = []
dir_and_sap=[]
[directors.append(d.director) for d in dirs]
[dir_all.append((d.director).split('@')[0]) for d in dirs]
[dir_and_sap.append([d.sap,(d.director).split('@')[0]]) for d in dirs]



error_sign_in = {'user': '', 'cause': ''}

events = {'sign_in': 'Вход в систему', 'get_feedback': 'Получен отзыв', 'upload': 'Загрузка HR файла', 
         'business_revenue_new_report': 'Скачивание отчета по продажам', 'business_open_alcohol_documents_report': 'Скачивание отчета по незакрытым документам приемки АП', 'business_open_documents': 'Незакрытые документы приемки',
        'business_open_documents_report': 'Скачивание отчета по незакрытым документам приемки', 'business_average_check_report': 'Скачивание отчета по среднему чеку', 
        'business_canceled_checks_report': 'Скачивание отчета по отмененным чекам', 'business_sellers_perfom_week_report': 'Скачивание отчета по скорости сканирования кассиров за неделю',
        'business_sellers_perfom_month_report': 'Скачивание отчета по скорости сканирования кассиров за месяц',
        'business_checks_traffic_report': 'Скачивание отчета по трафику чеков', 'business_old_price_report': 'Скачивание отчета по продажам по старой цене',
        'products_overdue_report': 'Скачивание отчета по просроченной продукции', 'products_alcohol_errors_report': 'Скачивание отчета по ошибкам продажи алкоголя',
        'products_low_saled_report': 'Скачивание отчета по товарам с низкими продажами', 'products_stoped_report': 'Скачивание отчета по товарам без движения',
        'products_stoped_nonfood_report': 'Скачивание отчета по товарам без движения NONFOOD', 'products_stoped_food_report': 'Скачивание отчета по товарам без движения FOOD',
        'products_stoped_fresh_report': 'Скачивание отчета по товарам без движения FRESH', 'products_minus_report': 'Скачивание отчета по товарам с отрицательными остатками',
        'products_topvd_report': 'Скачивание отчета по топ ВД', 'products_top30_report': 'Скачивание отчета по топ 30', 'products_super_price_report': 'Скачивание отчета по супер цене', 'index': 'Начальная страница', 
        'dashboard': 'Страница магазина', 'download_activity_log': 'Скачивание отчета по активности пользователей', 'download_feedback': 'Скачивание отчета по обратной связи',
        'do_logout': 'Выход из системы', 'go_back': 'Переход на страницу не своего магазина', 'nps_report': 'Скачивание отчета по NPS'}


@login_required(redirect_field_name='')
def get_date_nps(request):
    today = datetime.today() 
    tommorow = today + timedelta(days=1)
    today_str = datetime.strftime(today, '%Y-%m-%dT00:00:00')
    tommorow_str = datetime.strftime(tommorow, '%Y-%m-%dT00:00:00')
    date_start_end = {"start": today_str, "end": tommorow_str}
    return JsonResponse(date_start_end)

@login_required(redirect_field_name='')
def nps(request):
    mongo = pymongo.MongoClient('192.168.200.73', 27017)
    db = mongo['tcx']
    col = db['nps']
    cursor=col.find().sort("$natural",-1).limit(1)
    last_row_nps = None
    for i in cursor:
        last_row_nps=i["Last_Modified"]
    last_row_nps = last_row_nps.split("T")[0]
    last_row_nps_date = datetime.strptime(last_row_nps, '%Y-%m-%d')

    if last_row_nps_date.date() < datetime.today().date():
        records = json.loads(request.POST['nps_records'])    
        if datetime.today().date().day == 1 and (datetime.today().hour>22 and datetime.today().hour<23):
            col.remove({})
            col.insert_many(records)
        elif datetime.today().hour == 23:
            col.insert_many(records)
            mongo.close()  
    return JsonResponse({'output': 'success'}) 

@login_required(redirect_field_name='')
def kick_stores_page(request):
    return render(request, 'main/kick_stores.html')

@login_required(redirect_field_name='')
def kick_stores(request):
    output = ''
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=account.collector_ip, username=account.collector_user, password=account.collector_password)
        output = []
        i, o, e = client.exec_command('supervisorctl restart collector')
    return JsonResponse({'output': True}) 

@login_required(redirect_field_name='')
def kick_store(request):
    sap = request.POST['sap']
    output = ''
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=account.collector_ip, username=account.collector_user, password=account.collector_password)
        output = []
        errors = []
        i, o, e = client.exec_command('source collector/venv/bin/activate; python collector/kick_store.py ' + sap)
        output = o.read().decode('utf-8')
        errors = e.read().decode('utf-8')
    return JsonResponse({'output': output, 'errors': errors})       

@login_required(redirect_field_name='')
def heatmap_page(request):
    return render(request, 'main/heatmap' + sprint + version + '.html')

@login_required(redirect_field_name='')
def kpi_page_graph(request):
    return render(request, 'main/kpi_3_1.html')

@login_required(redirect_field_name='')
def get_heatmap(request):
    path = os.getcwd() + '/media/heatmap'
    now = time.time()
    for f in os.listdir(path):
        file_date = os.stat(os.path.join(path, f))
        if os.stat(os.path.join(path,f)).st_mtime < now - 1800:
            os.remove(os.path.join(path, f))
    result = json.loads(request.POST['data'])
    response = {}
    if result['status'] == 'day':
        start = datetime.strptime(result['date'] + ' ' + '00:00:00', '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(result['date'] + ' ' + '23:59:59', '%Y-%m-%d %H:%M:%S')
        heatmap.build_heatmap(start, end)
    elif result['status'] == 'period':
        start = datetime.strptime(result['start'] + ' ' + '00:00:00', '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(result['end'] + ' ' + '23:59:59', '%Y-%m-%d %H:%M:%S')
        if (end - start).days < 0:
            response['text'] ='Вы ввели неправильный период!'
            return JsonResponse(response)
        else:
            heatmap.build_heatmap(start, end)
    elif result['status'] == 'month':
        month = (result['month'].split('-'))[1]
        year = (result['month'].split('-'))[0]
        days = calendar.monthrange(int(year), int(month))[1]
        start = datetime.strptime(year + '-' + month + '-1 ' + '00:00:00', '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(year + '-' + month + '-' + str(days) + ' ' + '23:59:59', '%Y-%m-%d %H:%M:%S')
        heatmap.build_heatmap(start, end)
    else:
        start = datetime.strptime('2019-11-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        end = datetime.now()
        heatmap.build_heatmap(start, end)
    response['start'] = datetime.strftime(start, '%Y-%m-%d_%H-%M-%S')
    response['end'] = datetime.strftime(end, '%Y-%m-%d_%H-%M-%S')
    return JsonResponse(response)

@login_required(redirect_field_name='')
def get_kpi_graph(request):
    result = json.loads(request.POST['data'])
    response = {}

    if result['status'] == 'period':
        start = datetime.strptime(result['start'] + ' ' + '00:00:00', '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(result['end'] + ' ' + '23:59:59', '%Y-%m-%d %H:%M:%S')
        if (end - start).days < 0:
            response['text'] ='Вы ввели неправильный период!'
            return JsonResponse(response)
        else:
            kpi_4_1.create_kpi_graph(dir_all, start, end)
            kpi_4_1.get_result_activity(dir_and_sap, start, end)

    elif result['status'] == 'month':
        month = (result['month'].split('-'))[1]
        year = (result['month'].split('-'))[0]
        days = calendar.monthrange(int(year), int(month))[1]
        start = datetime.strptime(year + '-' + month + '-1 ' + '00:00:00', '%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(year + '-' + month + '-' + str(days) + ' ' + '23:59:59', '%Y-%m-%d %H:%M:%S')
        kpi_4_1.create_kpi_graph(start, end)
        kpi_4_1.get_result_activity(dir_and_sap, start, end)
   
    elif result['status'] == 'week':
        week = result['week']
        start = datetime.strptime(week + '-1', '%G-W%V-%u')
        end = start + timedelta(days=7)
        kpi_4_1.create_kpi_graph(dir_all, start, end)
        kpi_4_1.get_result_activity(dir_and_sap, start, end)

    else:
        start = datetime.strptime('2019-11-01 00:00:00', '%Y-%m-%d %H:%M:%S')
        end = datetime.now()
        kpi_4_1.create_kpi_graph(dir_all, start, end)
        kpi_4_1.get_result_activity(dir_and_sap, start, end)
    
    response['start'] = datetime.strftime(start, '%Y-%m-%d_%H-%M-%S')
    response['end'] = datetime.strftime(end, '%Y-%m-%d_%H-%M-%S')
    return JsonResponse(response)

@login_required(redirect_field_name='')
def get_feedback(request):
    response = {'connect': False, 'msg': ''}
    now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    user = request.user.username
    feedback = request.POST['feedback']
    sent_from = request.POST['sap']
    if ((user + '@x5.ru') in directors) or ((user) in directors):
        for d in dirs:
            if ((user + '@x5.ru') == d.director) or (user == d.director):
                sap = d.sap
    else:
        sap = ''
    mongo = pymongo.MongoClient('192.168.200.73', 27017)
    db = mongo['tcx']
    col = db['feedback']
    row = {'date': now, 'user': user, 'feedback': feedback}
    try:
        mongo.server_info()
        response['connect'] = True
        response['msg'] = 'Спасибо за отзыв!\nВаше сообщение отправлено!'
        row['sap'] = sap
        row['sent_from'] = sent_from
        row['status'] = 'Новое'
        col.insert_one(row)
    except:
        response['connect'] = False
        response['msg'] = 'К сожалению Ваше сообщение не отправлено!\nПопробуйте, пожалуйста, позже!'
    mongo.close()                                                                                                                                                                     
    return JsonResponse(response) 

@login_required(redirect_field_name='')
def upload_index(request):
    return render(request, 'main/upload' + sprint + version + '.html')

@login_required(redirect_field_name='')
def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage(os.getcwd() + '/media/')
        form = (uploaded_file.name).split('.')[1]
        name = 'hr_test'
        file_name = name + '.' + form
        if fs.exists(file_name) == False:
            if (form == 'xls') or (form == 'xlsx'):
                fs.save(file_name, uploaded_file)
                return redirect(request.path_info.split('upload')[0])
            else:
                return redirect(request.path_info.split('upload')[0])
        else:
            for j in os.walk(os.getcwd() + '/media/'):
                os.remove(j[0] + j[2][0])
            fs.save(file_name, uploaded_file)
            return redirect(request.path_info.split('upload')[0])

log_level = logging.INFO
LOG_PATH = os.getcwd() + "/logs/activity.csv"
logFormatter = logging.Formatter(fmt='%(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(log_level)
logfile = LOG_PATH
fileHandler = logging.FileHandler(logfile)
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(log_level)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rotateHandler = RotatingFileHandler(logfile, maxBytes=1024 * 1024 * 50, backupCount=1)
rotateHandler.setFormatter(logFormatter)
logger.addHandler(rotateHandler)


UDP_PORT = 514
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.connect(('192.168.70.200', UDP_PORT))
c = CEFEvent()

def mongo_log(function):   
    def wrapper(request, full_sap=None, click=None):
        date = datetime.now()  - timedelta(hours=3)
        user = request.user.username
        mongo = pymongo.MongoClient('192.168.200.73', 27017)
        db = mongo['tcx']
        col = db['logs']
        if full_sap:
            if click:
                col.insert_one({'date': date, 'user': user, 'action': 'click', 'sap': full_sap, 'block': click})
                mongo.close()  
                return function(request, full_sap, click)
            else:
                col.insert_one({'date': date, 'user': user, 'action': function.__name__, 'sap': full_sap, 'block': ''})
                mongo.close()
                return function(request, full_sap)
        else:
            col.insert_one({'date': date, 'user': user, 'action': function.__name__, 'sap': '', 'block': ''})
            mongo.close()
            return function(request)
    return wrapper

def cef_logging(function): 
    @wraps(function)  
    def wrapper(request, full_sap=None, click=None):
        time = str(datetime.now().time()).split('.')[0]
        date = str(datetime.now().date())
        f = open('media/cefevents_' + date + '.txt','a+')
        ip = request.META['REMOTE_ADDR']
        user = request.user.username
        if full_sap:
            if click:
                c.set_field('deviceVendor', 'Operational_DB_DM')
                c.set_field('deviceProduct', 'DB DM Test')
                c.set_field('severity', 4)
                c.set_field('end', date + ' ' + time)
                c.set_field('src', ip)
                c.set_field('duser', user)
                c.set_field('name', 'click')
                c.set_field('msg', 'store: ' + full_sap)
                c.set_field('click', click)
                c.build_cef()
                string = str(c)
                byte_string = bytes(string, 'utf-8')
                f.write(string + '\n')
                f.close()
                sock.send(byte_string)
                sleep(1)
                return function(request, full_sap, click)
            else:
                c.set_field('deviceVendor', 'Operational_DB_DM')
                c.set_field('deviceProduct', 'DB DM Test')
                c.set_field('severity', 4)
                c.set_field('end', date + ' ' + time)
                c.set_field('src', ip)
                c.set_field('duser', user)
                c.set_field('name', events[function.__name__])
                c.set_field('msg', 'store: ' + full_sap)
                c.build_cef()
                string = str(c)
                byte_string = bytes(string, 'utf-8')
                f.write(string + '\n')
                f.close()
                sock.send(byte_string)
                sleep(1)
                return function(request, full_sap)

        else:
            if function.__name__ == 'sign_in':
                if error_sign_in:
                    if error_sign_in['user']:
                        c.set_field('deviceVendor', 'Operational_DB_DM')
                        c.set_field('deviceProduct', 'DB DM Test')
                        c.set_field('severity', 4)
                        c.set_field('end', date + ' ' + time)
                        c.set_field('src', ip)
                        c.set_field('duser', error_sign_in['user'])
                        c.set_field('name', 'Неуспешная попытка входа (' + error_sign_in['cause'] + ')')
                        error_sign_in.clear()
                        c.build_cef()
                        string = str(c)
                        byte_string = bytes(string, 'utf-8')
                        f.write(string + '\n')
                        f.close()
                        sock.send(byte_string)
                        sleep(1)
            else:
                error_sign_in.clear()
                c.set_field('deviceVendor', 'Operational_DB_DM')
                c.set_field('deviceProduct', 'DB DM Test')
                c.set_field('severity', 4)
                c.set_field('end', date + ' ' + time)
                c.set_field('src', ip)
                c.set_field('duser', user)
                c.set_field('name', events[function.__name__])
                c.build_cef()
                string = str(c)
                byte_string = bytes(string, 'utf-8')
                f.write(string + '\n')
                f.close()
                sock.send(byte_string)
                sleep(1)
            return function(request)
    return wrapper


def do_logging(function):
    @wraps(function)
    def wrapper(request,full_sap=None, click=None):
        time = str(datetime.now().time()).split('.')[0]
        date = str(datetime.now().date())
        user = request.user.username
        if full_sap:
            if click:
                logger.info('{};{};{};{};{};{}'.format(date, time, request.user.username, 'click', full_sap, click))
                return function(request, full_sap, click)
            else:
                logger.info('{};{};{};{};{}'.format(date, time, request.user.username, function.__name__, full_sap))
                return function(request, full_sap)
        else:
            logger.info('{};{};{};{}'.format(date, time, request.user.username, function.__name__))
            return function(request)
    return wrapper


# # HR-показатели (отчет)
# @login_required(redirect_field_name='')
# def hr_indicators_original(request):
#     filename = 'hr_test.xlsx'
#     if os.listdir(path='media/'):
#         if filename in os.listdir(path='media/')[0]:
#             with open('media/hr_test.xlsx', 'rb') as fp:
#                 data = fp.read()
#         response = HttpResponse(content_type="application/")
#         response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
#         response.write(data)
#         return response



# ОСНОВНЫЕ БИЗНЕС ПОКАЗАТЕЛИ
# Продажи (новые)
@login_required(redirect_field_name='')
def business_revenue_new(request, full_sap):
    result = store_class.business_revenue_new(full_sap)
    return JsonResponse(result)

# Продажи (новые) (отчет)
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def business_revenue_new_report(request, full_sap):
    with open('reports/{0}/revenue_new_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_revenue_new_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response


# Приемка алкоголя(отчет)
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def business_open_alcohol_documents_report(request, full_sap):
    with open('reports/{0}/alcohol_documents_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_alcohol_documents_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Приемка алкоголя
@login_required(redirect_field_name='')
def business_open_alcohol_documents(request, full_sap):
    result = store_class.business_open_alcohol_documents(full_sap)
    return JsonResponse(result)


# # Незакрытие документы приемки(отчет)
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def business_open_documents_report(request, full_sap):
    with open('reports/{0}/open_documents_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_open_documents_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# # Незакрытие документы приемки
@login_required(redirect_field_name='')
def business_open_documents(request, full_sap):
    result = store_class.business_open_documents(full_sap)
    return JsonResponse(result)


# РТО
@login_required(redirect_field_name='')
def business_rto(request, full_sap):
    result = store_class.business_rto(full_sap)
    return JsonResponse(result)

# NPS
@login_required(redirect_field_name='')
def nps_from_mongo(request, full_sap):
    result = store_class.nps_from_mongo(full_sap)
    return JsonResponse(result)

@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def nps_report(request, full_sap):
    with open('reports/{0}/nps_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_nps_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response



# Средний чек(отчет)
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def business_average_check_report(request, full_sap):
    with open('reports/{0}/average_check_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_average_check_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Средний чек
@login_required(redirect_field_name='')
def business_average_check(request, full_sap):
    result = store_class.business_average_check(full_sap)
    return JsonResponse(result)


# Отмененные чеки(отчет)
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def business_canceled_checks_report(request, full_sap):
    with open('reports/{0}/cancel_check_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_cancel_check_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Отмененные чеки
@login_required(redirect_field_name='')
def business_canceled_checks(request, full_sap):
    result = store_class.business_canceled_checks(full_sap)
    return JsonResponse(result)


# Списания
@login_required(redirect_field_name='')
def business_write_offs(request, full_sap):
    result = store_class.business_write_offs(full_sap)
    return JsonResponse(result)


# Скорость сканирования кассиров(отчет)
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def business_sellers_perfom_week_report(request, full_sap):
    with open('reports/{0}/sellers_perfom_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_sellers_perfom_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Скорость сканирования кассиров(отчет за месяц)
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def business_sellers_perfom_month_report(request, full_sap):
    with open('reports/{0}/month_sellers_perfom_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_month_sellers_perfom_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Скорость сканирования кассиров
@login_required(redirect_field_name='')
def business_sellers_perfom(request, full_sap):
    result = store_class.business_sellers_perfom(full_sap)
    return JsonResponse(result)

# Трафик чеков (отчет)
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def business_checks_traffic_report(request, full_sap):
    with open('reports/{0}/checks_traffic_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_checks_traffic_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Трафик чеков
@login_required(redirect_field_name='')
def business_checks_traffic(request, full_sap):
    result = store_class.business_checks_traffic(full_sap)
    return JsonResponse(result)

# Продажи по старой цене (отчет)
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def business_old_price_report(request, full_sap):
    with open('reports/{0}/old_price_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_old_price_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Продажи по старой цене 
@login_required(redirect_field_name='')
def business_old_price(request, full_sap):
    result = store_class.business_old_price(full_sap)
    return JsonResponse(result)


# # # HR показатели (отчет)
# @login_required(redirect_field_name='')
# @mongo_log
# @cef_logging
# @do_logging
# def hr_indicators_report(request, full_sap):
#     with open('reports/{0}/hr_indicators_report.xlsx'.format(full_sap), 'rb') as fp:
#         data = fp.read()
#     filename = '{}_hr_indicators_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
#     response = HttpResponse(content_type="application/")
#     response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
#     response.write(data)
#     return response

# # HR показатели
@login_required(redirect_field_name='')
def hr_indicators(request, full_sap):
    result = store_class.hr_indicators(full_sap)
    return JsonResponse(result)

# Markdown
@login_required(redirect_field_name='')
def business_markdown(request, full_sap):
    result = store_class.business_markdown(full_sap)
    return JsonResponse(result)


# ТОВАРЫ
# Просроченая продукция(отчет)
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def products_overdue_report(request, full_sap):
    with open('reports/{0}/overdue_products_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_overdue_products_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Просроченая продукция
@login_required(redirect_field_name='')
def products_overdue(request, full_sap):
    result = store_class.products_overdue(full_sap)
    return JsonResponse(result)


# Ошибки продажи алкоголя(отчет)
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def products_alcohol_errors_report(request, full_sap):
    with open('reports/{0}/alcohol_errors_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_alcohol_errors_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Ошибки продажи алкоголя
@login_required(redirect_field_name='')
def products_alcohol_errors(request, full_sap):
    result = store_class.products_alcohol_errors(full_sap)
    return JsonResponse(result)


# Товары с низкими продажами(отчет)
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def products_low_saled_report(request, full_sap):
    with open('reports/{0}/low_saled_products_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_low_saled_products_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Товары с низкими продажами
@login_required(redirect_field_name='')
def products_low_saled(request, full_sap):
    result = store_class.products_low_saled(full_sap)
    return JsonResponse(result)


# Товары без движения(отчет)
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def products_stoped_report(request, full_sap):
    with open('reports/{0}/stoped_products_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_stoped_products_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def products_stoped_food_report(request, full_sap):
    with open('reports/{0}/stoped_products_food_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_stoped_products_food_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def products_stoped_nonfood_report(request, full_sap):
    with open('reports/{0}/stoped_products_nonfood_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_stoped_products_nonfood_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def products_stoped_fresh_report(request, full_sap):
    with open('reports/{0}/stoped_products_fresh_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_stoped_products_fresh_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Товары без движения
@login_required(redirect_field_name='')
def products_stoped(request, full_sap):
    result = store_class.products_stoped(full_sap)
    return JsonResponse(result)

@login_required(redirect_field_name='')
def products_stoped_food(request, full_sap):
    result = store_class.products_stoped_food(full_sap)
    return JsonResponse(result)

@login_required(redirect_field_name='')
def products_stoped_nonfood(request, full_sap):
    result = store_class.products_stoped_nonfood(full_sap)
    return JsonResponse(result)

@login_required(redirect_field_name='')
def products_stoped_fresh(request, full_sap):
    result = store_class.products_stoped_fresh(full_sap)
    return JsonResponse(result)


# Товары с отрицательными остатками(отчет)
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def products_minus_report(request, full_sap):
    with open('reports/{0}/minus_products_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_minus_products_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Товары с отрицательными остатками
@login_required(redirect_field_name='')
def products_minus(request, full_sap):
    result = store_class.products_minus(full_sap)
    return JsonResponse(result)

@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def products_top30_report(request, full_sap):
    with open('reports/{0}/top30_products_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_top30_products_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Топ 30
@login_required(redirect_field_name='')
def products_top30(request, full_sap):
    result = store_class.products_top30(full_sap)
    return JsonResponse(result)

@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def products_super_price_report(request, full_sap):
    with open('reports/{0}/super_price_products_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_super_price_products_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Супер цена
@login_required(redirect_field_name='')
def products_super_price(request, full_sap):
    result = store_class.products_super_price(full_sap)
    return JsonResponse(result)

@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def products_topvd_report(request, full_sap):
    with open('reports/{0}/topvd_products_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_topvd_products_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Топ ВД
@login_required(redirect_field_name='')
def products_topvd(request, full_sap):
    result = store_class.products_topvd(full_sap)
    return JsonResponse(result)




# ДОСТУПНОСТЬ ОСНОВНЫХ СЕРВИСОВ
# Cвязь
@login_required(redirect_field_name='')
def services_net(request, full_sap):
    result = store_class.services_net(full_sap)
    return JsonResponse(result)


# Алкоголь
@login_required(redirect_field_name='')
def services_alcohol(request, full_sap):
    result = store_class.services_alcohol(full_sap)
    return JsonResponse(result)


# Лояльность
@login_required(redirect_field_name='')
def services_loyalty(request, full_sap):
    result = store_class.services_loyalty(full_sap)
    return JsonResponse(result)


# Безналичный расчет
@login_required(redirect_field_name='')
def services_cashless(request, full_sap):
    result = store_class.services_cashless(full_sap)
    return JsonResponse(result)




# ГЛАВНАЯ
@login_required(redirect_field_name='')
@cef_logging
def index(request):
    if ((request.user.username + '@x5.ru') in directors) or ((request.user.username) in directors):
        for d in dirs:
            if ((request.user.username + '@x5.ru') == d.director) or (request.user.username) == d.director:
                store = store_class.get_full_sap(d.sap)['sap']
                if request.method == 'POST':
                    return redirect('dashboard', store)
                else:
                    return redirect('dashboard', store)
    else:
        if request.method == 'POST':
            search = request.POST.get('store').upper()
            store = store_class.get_full_sap(search)
            if store == None:
                messages.warning(request, 'Вы ввели неверный магазин!')
                return redirect(index)
            else:
                return redirect('dashboard', store['sap'])
        else:
            return render(request, 'main/index' + sprint + version + '.html')



# КАССЫ
@login_required(redirect_field_name='') 
def poses(request, full_sap):
    poses = store_class.poses(full_sap)
    return JsonResponse(poses)




# КСО
@login_required(redirect_field_name='')
def kso(request, full_sap):
    kso = store_class.kso(full_sap)
    return JsonResponse(kso)




# ВЕСЫ
@login_required(redirect_field_name='')
def scales(request, full_sap):
    scales = store_class.scales(full_sap)
    return JsonResponse(scales)

# Обратная связь
@login_required(redirect_field_name='')
def feedback(request):
    feedback = store_class.feedback()
    return JsonResponse(feedback, safe=False)


# ДАШБОРД
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def dashboard(request, full_sap):
    if request.method == 'POST':
        if ((request.user.username + '@x5.ru') in directors) or ((request.user.username) in directors):
            for d in dirs:
                if ((request.user.username + '@x5.ru') == d.director) or ((request.user.username) == d.director):
                    search = request.POST.get('store').upper()
                    if search == d.sap:
                        store = store_class.get_full_sap(search)['sap']
                        return redirect('dashboard', store)
                    else:
                        return render(request, 'main/access' + sprint + version + '.html', {
                                                        'full_sap': store_class.get_full_sap(search)['sap'],
                                                        })
        else:
            search = request.POST.get('store').upper()
            store = store_class.get_full_sap(search)
            if store == None:
                messages.warning(request, 'Вы ввели неверный магазин!')
                return redirect('dashboard', full_sap)
            else:
                return redirect('dashboard', store['sap'])
    else:
        if ((request.user.username + '@x5.ru') in directors) or ((request.user.username) in directors):
            for d in dirs:
                if ((request.user.username + '@x5.ru') == d.director) or ((request.user.username) == d.director):
                    if full_sap == store_class.get_full_sap(d.sap)['sap']:
                        return render(request, 'main/dashboard' + sprint + version + '.html', {
                                                    'full_sap': full_sap,
                                                    })
                    else:
                        return render(request, 'main/access' + sprint + version + '.html', {
                                                        'full_sap': full_sap,
                                                        })
        else:
            return render(request, 'main/dashboard' + sprint + version + '.html', {
                                                    'full_sap': full_sap,
                                                    })

def sap_name(request, full_sap):
    name = store_class.get_full_sap(full_sap)['name']
    return JsonResponse(name, safe=False)



# ЛОГИРОВАНИЕ
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def download_activity_log(request):
    header = ["Дата", "Время", "Пользователь", "Действие", "SAP №", 'Блок']
    with open(os.getcwd() + '/logs/activity.csv', 'r') as fp:
        data = fp.readlines()
    workbook = xlsxwriter.Workbook(os.getcwd() + '/logs/activity.xlsx')
    worksheet = workbook.add_worksheet()
    col = 0
    for h in header:
        worksheet.write_string(0, col, str(h).capitalize())
        col += 1
    col = 0
    row = 1
    for d in data:
        l = d.split(';')
        for i, v in enumerate(l):
            worksheet.write_string(row, col+i, str(v).capitalize())
        row += 1
    workbook.close()
    with open(os.getcwd() + "/logs/activity.xlsx", "rb") as fp:
        data = fp.read()
    os.remove(os.getcwd() + "/logs/activity.xlsx")
    filename = 'activity.xlsx'
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# ОБРАТНАЯ СВЯЗЬ
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def download_feedback(request):
    mongo = pymongo.MongoClient('192.168.200.73', 27017)
    db = mongo['tcx']
    collection = db['feedback']
    result = collection.find({})
    data = [[record['date'], record['user'], record['sap'], record['sent_from'], record['feedback'], record['status']] for record in result]
    header = ["Дата", "Пользователь", "SAP", "Отправлено с", "Сообщение", "Статус"]
    workbook = xlsxwriter.Workbook(os.getcwd() + '/logs/feedback.xlsx')
    worksheet = workbook.add_worksheet()
    col = 0
    for h in header:
        worksheet.write_string(0, col, str(h).capitalize())
        col += 1
    col = 0
    row = 1
    for d in data:
        for i in range(len(d)):
            worksheet.write_string(row, col+i, str(d[i]).capitalize())
        row += 1
    workbook.close()
    with open(os.getcwd() + "/logs/feedback.xlsx", "rb") as fp:
        data = fp.read()
    os.remove(os.getcwd() + "/logs/feedback.xlsx")
    filename = 'feedback.xlsx'
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response


# АВТОРИЗАЦИЯ
@cef_logging
def sign_in(request):
    if request.user.is_authenticated:
        return redirect(index)
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username'].lower()
                password = form.cleaned_data['password']
                if username == 'admin':
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect(index)
                else:
                    if '@' in username:
                        username = username.split('@')[0]
                    if checkUserInAD(username+'@x5.ru', password):
                        if checkUserGroup(username+'@x5.ru', password):
                            user = authenticate(request, username=username, password=password)
                            if user is not None:
                                if ((username + '@x5.ru') in directors) or (username in directors): 
                                    for d in dirs:
                                        if ((username + '@x5.ru') == d.director) or ((username) == d.director):
                                            store = d.sap
                                            if (d.last_name == ''):
                                                user.last_name = (d.director).split('@')[0]
                                            else:
                                                user.last_name = d.last_name
                                                user.first_name = d.name
                                            user.save()
                                            login(request, user)
                                            return redirect('dashboard', store_class.get_full_sap(store)['sap'])
                                else:
                                    login(request, user)
                                    return redirect(index)
                            else:
                                if ((username + '@x5.ru') in directors) or ((username) in directors): 
                                    for d in dirs:
                                        if (username + '@x5.ru') == d.director:
                                            user = User.objects.create_user(username, username+'@x5.ru', password)
                                            if (d.last_name == ''):
                                                user.last_name = (d.director).split('@')[0]
                                            else:
                                                user.first_name = d.name
                                                user.last_name = d.last_name
                                            user.save()
                                            login(request, user)
                                            return redirect('dashboard', store_class.get_full_sap(d.sap)['sap'])
                                        elif (username) == d.director:
                                            user = User.objects.create_user(username, username, password)
                                            if (d.last_name == ''):
                                                user.last_name = (d.director).split('@')[0]
                                            else:
                                                user.first_name = d.name
                                                user.last_name = d.last_name
                                            user.save()
                                            login(request, user)
                                            return redirect('dashboard', store_class.get_full_sap(d.sap)['sap'])
                                else:
                                    if User.objects.filter(username=username).exists():
                                        user = User.objects.get(username__exact=username)
                                        user.set_password(password)
                                        user.save()
                                        login(request, user)
                                        return redirect(index)
                                    else:
                                        user = User.objects.create_user(username, username+'@x5.ru', password)
                                        user.first_name = username
                                        user.save()
                                        login(request, user)
                                        return redirect(index)
                            
                        else:
                            messages.error(request, 'У вас нет доступа к данному сайту. Чтобы запросить доступ к сайту, обратитесь на DASHBOARD-DIR-PRODUCT@X5.RU')
                            error_sign_in['user'] = username
                            error_sign_in['cause'] = 'Пользователя нет в системе'
                            return redirect(sign_in)
                    else:
                        messages.error(request, 'Неверный логин/пароль')
                        error_sign_in['user'] = username
                        error_sign_in['cause'] = 'Неверный пароль'
                        return redirect(sign_in)
            else:
                messages.error(request, 'Неверный логин/пароль')
                return redirect(sign_in)
        else:
            form = LoginForm()
    return render(request, 'main/sign_in' + sprint + version + '.html', {'form':form})




# ВЫХОД
@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def do_logout(request):
    logout(request)
    return redirect(sign_in)


@login_required(redirect_field_name='')
@mongo_log
@do_logging
def click_detect(request, full_sap, action):
    return HttpResponse()

@login_required(redirect_field_name='')
@mongo_log
@cef_logging
@do_logging
def go_back(request, full_sap):
    for d in dirs:
        if ((request.user.username + '@x5.ru') == d.director) or ((request.user.username) == d.director):
                return redirect('dashboard', store_class.get_full_sap(d.sap)['sap'])


