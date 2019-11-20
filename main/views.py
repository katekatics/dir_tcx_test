from django.shortcuts import render, redirect
from . import store_class
from .models import Message, Incident
from django.contrib.auth.decorators import login_required
from .ad import checkUserInAD
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm
from django.http import JsonResponse
from datetime import datetime
import os
from django.http import HttpResponse, HttpResponseRedirect
import xlsxwriter
from django.core.files.storage import FileSystemStorage
import shutil

# LOGGER
import logging
from logging.handlers import RotatingFileHandler

@login_required
def upload_index(request):
    return render(request, 'main/upload.html')

@login_required
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


def do_logging(function):
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

# HR-показатели (отчет)
@login_required
def hr_indicators_original(request):
    filename = 'hr_test.xlsx'
    if os.listdir(path='media/'):
        if filename in os.listdir(path='media/')[0]:
            with open('media/hr_test.xlsx', 'rb') as fp:
                data = fp.read()
        response = HttpResponse(content_type="application/")
        response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
        response.write(data)
        return response



# ОСНОВНЫЕ БИЗНЕС ПОКАЗАТЕЛИ
# Продажи
@login_required
def business_revenue(request, full_sap):
    result = store_class.business_revenue(full_sap)
    return JsonResponse(result)


# Приемка алкоголя(отчет)
@login_required
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
@login_required
def business_open_alcohol_documents(request, full_sap):
    result = store_class.business_open_alcohol_documents(full_sap)
    return JsonResponse(result)


# # Незакрытие документы приемки(отчет)
@login_required
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
@login_required
def business_open_documents(request, full_sap):
    result = store_class.business_open_documents(full_sap)
    return JsonResponse(result)


# РТО
@login_required
def business_rto(request, full_sap):
    result = store_class.business_rto(full_sap)
    return JsonResponse(result)


# Средний чек(отчет)
@login_required
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
@login_required
def business_average_check(request, full_sap):
    result = store_class.business_average_check(full_sap)
    return JsonResponse(result)


# Отмененные чеки(отчет)
@login_required
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
@login_required
def business_canceled_checks(request, full_sap):
    result = store_class.business_canceled_checks(full_sap)
    return JsonResponse(result)


# Списания
@login_required
def business_write_offs(request, full_sap):
    result = store_class.business_write_offs(full_sap)
    return JsonResponse(result)


# Скорость сканирования кассиров(отчет)
@login_required
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
@login_required
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
@login_required
def business_sellers_perfom(request, full_sap):
    result = store_class.business_sellers_perfom(full_sap)
    return JsonResponse(result)


# # HR показатели (отчет)
@login_required
@do_logging
def hr_indicators_report(request, full_sap):
    with open('reports/{0}/hr_indicators_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_hr_indicators_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# # HR показатели
@login_required
def hr_indicators(request, full_sap):
    result = store_class.hr_indicators(full_sap)
    return JsonResponse(result)

# Markdown
@login_required
def business_markdown(request, full_sap):
    result = store_class.business_markdown(full_sap)
    return JsonResponse(result)


# ТОВАРЫ
# Просроченая продукция(отчет)
@login_required
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
@login_required
def products_overdue(request, full_sap):
    result = store_class.products_overdue(full_sap)
    return JsonResponse(result)


# Ошибки продажи алкоголя(отчет)
@login_required
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
@login_required
def products_alcohol_errors(request, full_sap):
    result = store_class.products_alcohol_errors(full_sap)
    return JsonResponse(result)


# Товары с низкими продажами(отчет)
@login_required
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
@login_required
def products_low_saled(request, full_sap):
    result = store_class.products_low_saled(full_sap)
    return JsonResponse(result)


# Товары без движения(отчет)
@login_required
@do_logging
def products_stoped_report(request, full_sap):
    with open('reports/{0}/stoped_products_report.xlsx'.format(full_sap), 'rb') as fp:
        data = fp.read()
    filename = '{}_stoped_products_report_{}.xlsx'.format(full_sap, str(datetime.now().date()))
    response = HttpResponse(content_type="application/")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename # force browser to download file
    response.write(data)
    return response

# Товары без движения
@login_required
def products_stoped(request, full_sap):
    result = store_class.products_stoped(full_sap)
    return JsonResponse(result)


# Товары с отрицательными остатками(отчет)
@login_required
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
@login_required
def products_minus(request, full_sap):
    result = store_class.products_minus(full_sap)
    return JsonResponse(result)




# ДОСТУПНОСТЬ ОСНОВНЫХ СЕРВИСОВ
# Cвязь
@login_required
def services_net(request, full_sap):
    result = store_class.services_net(full_sap)
    return JsonResponse(result)


# Алкоголь
@login_required
def services_alcohol(request, full_sap):
    result = store_class.services_alcohol(full_sap)
    return JsonResponse(result)


# Лояльность
@login_required
def services_loyalty(request, full_sap):
    result = store_class.services_loyalty(full_sap)
    return JsonResponse(result)


# Безналичный расчет
@login_required
def services_cashless(request, full_sap):
    result = store_class.services_cashless(full_sap)
    return JsonResponse(result)




# ГЛАВНАЯ
@login_required
def index(request):
    if request.method == 'POST':
        search = request.POST.get('store').upper()
        store = store_class.get_full_sap(search)
        return redirect('dashboard', store)
    else:
        return render(request, 'main/index.html')




# КАССЫ
@login_required   
def poses(request, full_sap):
    poses = store_class.poses(full_sap)
    return JsonResponse(poses)




# КСО
@login_required
def kso(request, full_sap):
    kso = store_class.kso(full_sap)
    return JsonResponse(kso)




# ВЕСЫ
@login_required
def scales(request, full_sap):
    scales = store_class.scales(full_sap)
    return JsonResponse(scales)




# ДАШБОРД
@login_required
@do_logging
def dashboard(request, full_sap):
    if request.method == 'POST':
        search = request.POST.get('store').upper()
        store = store_class.get_full_sap(search)
        return redirect('dashboard', store)
    else:
        store = store_class.get_full_sap(full_sap)
        return render(request, 'main/dashboard.html', {
                                                    'full_sap': full_sap,
                                                    })



# ЛОГИРОВАНИЕ
@login_required
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



# АВТОРИЗАЦИЯ
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
                        user = authenticate(request, username=username, password=password)
                        if user is not None:
                            login(request, user)
                            if 'next' in request.GET:
                                return HttpResponseRedirect(request.GET['next'])
                            return redirect(index)
                        else:
                            if User.objects.filter(username=username).exists():
                                user = User.objects.get(username__exact=username)
                                user.set_password(password)
                                user.save()
                                login(request, user)
                                return redirect(index)
                            else:
                                user = User.objects.create_user(username, username+'@x5.ru', password)
                                user.save()
                                login(request, user)
                                return redirect(index)
                    else:
                        return redirect(sign_in)
            else:
                return redirect(sign_in)
        else:
            form =LoginForm()
    return render(request, 'main/sign_in.html', {'form':form})




# ВЫХОД
@login_required
@do_logging
def do_logout(request):
    logout(request)
    return redirect(sign_in)


@login_required
@do_logging
def click_detect(request, full_sap, action):
    return HttpResponse()

# def process_request(request):
    # last_activity = request.session['user']