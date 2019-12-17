from pyzabbix import ZabbixAPI
import os
import cx_Oracle
import time
from datetime import datetime, timedelta
import requests
from . import account
import xlsxwriter
import subprocess
import platform
import pymongo


bf_rule1 = ('1', '2', 'B')
bf_rule2 = ('4000', '4001', '4002', '4003', '4004', '4005', '4006')

os.environ['PATH'] = 'C:\oracle\instantclient_19_3/'
# ОСНОВНЫЕ БИЗНЕС ПОКАЗАТЕЛИ
# Продажи

def find_errors(store):
    mongo = pymongo.MongoClient('192.168.200.73', 27017)
    db = mongo['tcx']
    collection = db['update_time']
    find = collection.find_one({"host": store['host']})
    if find:
        store['errors'] = find['errors']
    else:
        store['errors'] = []
    return store


def find_data(col, store):
    mongo = pymongo.MongoClient('192.168.200.73', 27017)
    db = mongo['tcx']
    collection = db[col]
    find = collection.find_one({"host": store})
    if find:
        find['_id'] = str(find['_id'])
        mongo.close()
        find['date'] += timedelta(hours=3)
        find['date'] = find['date'].strftime("%Y-%m-%d %H:%M:%S")
        find = find_errors(find)
    else:
        find = find_errors({"host": store})
    return find


def business_revenue(store):
    return find_data('business_revenue', store)

def business_revenue_new(store):
    result = find_data('business_revenue_new', store)
    if 'thead' in result:
        write_report('business_revenue_new_report',
                    result['thead'], result['tbody'], store)
    return result


# Незакрытие документы приемки алкоголя
def business_open_alcohol_documents(store):
    result = find_data('business_open_alcohol_documents', store)
    if 'thead' in result:
        write_report('alcohol_documents_report',
                    result['thead'], result['tbody'], store)
    return result


# Незакрытие документы приемки
def business_open_documents(store):
    result = find_data('business_open_documents', store)
    if 'thead' in result:
        write_report('open_documents_report',
                    result['thead'], result['tbody'], store)
    return result


# РТО
def business_rto(store):
    result = find_data('business_rto', store)
    return result


# Средний чек
def business_average_check(store):
    result = find_data('business_avg_check', store)
    if 'thead' in result:
        write_report('average_check_report',
                    result['thead'], result['tbody'], store)
    return result


# Списания
def business_write_offs(store):
    result = find_data('business_write_offs', store)
    return result

# Отмененные чеки


def business_canceled_checks(store):
    result = find_data('business_canceled_checks', store)
    if 'thead' in result:
        write_report('cancel_check_report',
                    result['thead'], result['tbody'], store)
    return result


# Скорость сканирования кассиров
def business_sellers_perfom(store):
    result = find_data('business_sellers_perfom', store)
    if 'thead' in result:
        write_report('sellers_perfom_report',
                    result['thead'], result['day'], store)
        write_report('month_sellers_perfom_report',
                    result['thead'], result['month'], store)
    return result

# HR показатели
def hr_indicators(store):
    result = find_data('hr_indicators', store)
    if 'thead' in result:
        write_report('hr_indicators_report',
                    result['thead'], result['tbody'], store)
    return result

# Markdown
def business_markdown(store):
    result = find_data('business_markdown', store)
    return result


# ТОВАРЫ

# Просроченая продукция
def products_overdue(store):
    result = find_data('products_overdue_new', store)
    if 'thead' in result:
        write_report('overdue_products_report',
                    result['thead'], result['tbody'], store)
    return result


# Ошибки продажи алкоголя
def products_alcohol_errors(store):
    result = find_data('products_alcohol_errors', store)
    return result


# Товары с низкими продажами
def products_low_saled(store):
    result = find_data('products_low_saled', store)
    if 'thead' in result:
        write_report('low_saled_products_report',
                    result['thead'], result['tbody'], store)
    return result


# Товары без движения
def products_stoped(store):
    result = find_data('products_stoped', store)
    if 'thead' in result:
        write_report('stoped_products_report',
                    result['thead'], result['tbody'], store)
    return result

def products_stoped_food(store):
    result = find_data('products_stoped_food', store)
    if 'thead' in result:
        write_report('stoped_products_food_report',
                    result['thead'], result['tbody'], store)
    return result

def products_stoped_nonfood(store):
    result = find_data('products_stoped_nonfood', store)
    if 'thead' in result:
        write_report('stoped_products_nonfood_report',
                    result['thead'], result['tbody'], store)
    return result

def products_stoped_fresh(store):
    result = find_data('products_stoped_fresh', store)
    if 'thead' in result:
        write_report('stoped_products_fresh_report',
                    result['thead'], result['tbody'], store)
    return result


# Товары с отрицательными остатками
def products_minus(store):
    result = find_data('products_minus', store)
    if 'thead' in result:
        write_report('top30_products_report',
                    result['thead'], result['tbody'], store)
    return result

# Топ 30
def products_top30(store):
    result = find_data('products_top30', store)
    if 'thead' in result:
        write_report('top30_products_report',
                    result['thead'], result['tbody'], store)
    return result

# Топ ВД
def products_topvd(store):
    result = find_data('products_topvd', store)
    if 'thead' in result:
        write_report('topvd_products_report',
                    result['thead'], result['tbody'], store)
    return result


# ДОСТУПНОСТЬ ОСНОВНЫХ СЕРВИСОВ
# Cвязь
def services_net(store):
    result = find_data('services_net', store)
    return result


# Алкоголь
def services_alcohol(store):
    result = find_data('services_alcohol', store)
    return result


# Лояльность
def services_loyalty(store):
    result = find_data('services_loyalty', store)
    return result


# Безналичный расчет
def services_cashless(store):
    result = find_data('services_cashless', store)
    return result





def poses(store):
    result = find_data('poses', store)
    offline = 0
    if 'poses' in result:
        for i, v in enumerate(result['poses']):
            if ping(v['ip']):
                result['poses'][i]['theme'] = 'card bg-success text-white my-1'
            else:
                offline += 1
                result['poses'][i]['theme'] = 'card bg-dark text-white my-1'
        if offline / len(result['poses']) <= 0.2:
            result['theme'] = 'card-header bg-success text-white'
        elif 0.2 < offline / len(result['poses']) < 0.6:
            result['theme'] = 'card-header bg-warning text-white'
        elif offline / len(result['poses']) >= 0.6:
            poses['theme'] = 'card-header bg-danger text-white'
    return result




# Весы
def scales(store):
    result = find_data('scales', store)
    offline = 0
    if 'scales' in result:
        for i, v in enumerate(result['scales']):
            if not ping(v['ip']):
                result['scales'][i]['theme'] = 'card bg-dark text-white my-1'
                offline += 1
            elif v['delta'] >= 43200:
                result['scales'][i]['theme'] = 'card bg-danger text-white my-1'
            elif v['delta'] >= 21600:
                result['scales'][i]['theme'] = 'card bg-warning text-white my-1'
            else:
                result['scales'][i]['theme'] = 'card bg-success text-white my-1'
        if offline/len(result['scales']) >= 0.5:
            result['theme'] = 'card-header bg-danger text-white'
        elif offline/len(result['scales']) >= 0.25:
            result['theme'] = 'card-header bg-warning text-white'
        else:
            result['theme'] = 'card-header bg-success text-white'
        result['scales'] = sorted(result['scales'], key = lambda i: i['name'])
    return result



# КСО
def kso(store):
    result = find_data('kso', store)
    offline = 0
    if 'kso' in result:
        for i, v in enumerate(result['kso']):
            if ping(v['ip']):
                result['kso'][i]['theme'] = 'card bg-success text-white my-1'
            else:
                offline += 1
                result['kso'][i]['theme'] = 'card bg-dark text-white my-1'
        if result['kso']:
            if offline / len(result['kso']) <= 0.2:
                result['theme'] = 'card-header bg-success text-white'
            elif 0.2 < offline / len(result['kso']) < 0.6:
                result['theme'] = 'card-header bg-warning text-white'
            elif offline / len(result['kso']) >= 0.6:
                result['theme'] = 'card-header bg-danger text-white'
        else:
            result['theme'] = 'card-header bg-danger text-white'
    return result




# Технические

def ping(ip):
    com = 'ping' if platform.system().lower() == 'windows' else '/bin/ping'
    count = '-n' if platform.system().lower() == 'windows' else '-c'
    timeout = '-w' if platform.system().lower() == 'windows' else '-W'
    timeout_count = '1000' if platform.system().lower() == 'windows' else '1'
    command = [com, count, '2', timeout, timeout_count, ip]
    return subprocess.call(command, stdout=subprocess.PIPE) == 0


def write_report(name, header, data, store):
    if not os.path.exists('reports/'):
        os.mkdir('reports/')
    if not os.path.exists('reports/{}'.format(str(store))):
        os.mkdir('reports/{}'.format(str(store)))
    workbook = xlsxwriter.Workbook(
        'reports/{0}/{1}.xlsx'.format(str(store), name))
    worksheet = workbook.add_worksheet()
    col = 0
    for h in header:
        worksheet.write_string(0, col, str(h).capitalize())
        col += 1
    col = 0
    row = 1
    for d in data:
        for i, v in enumerate(d):
            worksheet.write_string(row, col+i, str(v).capitalize())
        row += 1
    workbook.close()


def get_bd_ip(store):
    store = get_full_sap(store)
    db = get_interfaces(store)
    return db


def get_full_sap(store):
    if store.upper().startswith("SUPER") or store.upper().startswith(bf_rule1) or store.upper() in bf_rule2:
        zabbix = ZabbixAPI('http://zabbix-head.x5.ru/')
        zabbix.login(account.zabbix_login, account.zabbix_pass)
        find = zabbix.do_request('host.get', {
            'search': {
                'name': store
            },
            'monitored_hosts': 'true',
            'output': ['name']
        })['result']
        zabbix.session.close()
        if find:
            for i in find:
                if i['name'].startswith('Super'):
                    return i['name']

def get_hostid(store):
    if store.upper().startswith("SUPER") or store.upper().startswith(bf_rule1) or store.upper() in bf_rule2:
        zabbix = ZabbixAPI('http://zabbix-head.x5.ru/')
        zabbix.login(account.zabbix_login, account.zabbix_pass)
        find = zabbix.do_request('host.get', {
            'search': {
                'name': store
            },
            'monitored_hosts': 'true',
            'output': ['name']
        })['result']
        zabbix.session.close()
        if find:
            return find[0]['hostid']


def get_interfaces(store):
    interfaces = []
    zabbix = ZabbixAPI('http://zabbix-head.x5.ru/')
    zabbix.login(account.zabbix_login, account.zabbix_pass)
    find = zabbix.do_request('host.get', {
        'search': {
            'name': store
        },
        'selectInterfaces': ['ip', 'dns'],
        'output': 'extend'
    })['result']
    zabbix.session.close()
    interfaces = [{'ip': i['ip'], 'name': i['dns']}
                  for i in find[0]['interfaces']]
    for i in interfaces:
        if i['name'].startswith('CASH'):
            return '.'.join(i['ip'].split('.')[:-1]) + '.10'
            # ip = '.'.join(i['ip'].split('.')[:-1])


def raz_del(x):
    return '{0:,}'.format(x).replace(',', ' ')
