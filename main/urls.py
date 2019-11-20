from django.urls import path
from . import views


urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('store/<str:full_sap>/products_low_saled_report/', views.products_low_saled_report, name='products_low_saled_report'),
    path('store/<str:full_sap>/products_low_saled/', views.products_low_saled, name='products_low_saled'),

    path('store/<str:full_sap>/products_stoped_report/', views.products_stoped_report, name='products_stoped_report'),
    path('store/<str:full_sap>/products_stoped/', views.products_stoped, name='products_stoped'),

    path('store/<str:full_sap>/products_minus_report/', views.products_minus_report, name='products_minus_report'),
    path('store/<str:full_sap>/products_minus/', views.products_minus, name='products_minus'),

    path('store/<str:full_sap>/products_overdue_report/', views.products_overdue_report, name='products_overdue_report'),
    path('store/<str:full_sap>/products_overdue/', views.products_overdue, name='products_overdue'),

    path('store/<str:full_sap>/products_alcohol_errors_report/', views.products_alcohol_errors_report, name='products_alcohol_errors_report'),
    path('store/<str:full_sap>/products_alcohol_errors/', views.products_alcohol_errors, name='products_alcohol_errors'),

    path('store/<str:full_sap>/business_sellers_perfom_month_report/', views.business_sellers_perfom_month_report, name='business_sellers_perfom_month_report'),
    path('store/<str:full_sap>/business_sellers_perfom_week_report/', views.business_sellers_perfom_week_report, name='business_sellers_perfom_week_report'),
    path('store/<str:full_sap>/business_sellers_perfom/', views.business_sellers_perfom, name='business_sellers_perfom'),

    path('store/<str:full_sap>/business_average_check_report/', views.business_average_check_report, name='business_average_check_report'),
    path('store/<str:full_sap>/business_average_check/', views.business_average_check, name='business_average_check'),

    path('store/<str:full_sap>/business_canceled_checks_report/', views.business_canceled_checks_report, name='business_canceled_checks_report'),
    path('store/<str:full_sap>/business_canceled_checks/', views.business_canceled_checks, name='business_canceled_checks'),

    path('store/<str:full_sap>/business_open_alcohol_documents_report/', views.business_open_alcohol_documents_report, name='business_open_alcohol_documents_report'),
    path('store/<str:full_sap>/business_open_alcohol_documents/', views.business_open_alcohol_documents, name='business_open_alcohol_documents'),

    path('store/<str:full_sap>/business_open_documents_report/', views.business_open_documents_report, name='business_open_documents_report'),
    path('store/<str:full_sap>/business_open_documents/', views.business_open_documents, name='business_open_documents'),

    path('click_detect/<str:full_sap>/<str:click>/', views.click_detect, name='click_detect'),
    path('download_activity_log/', views.download_activity_log, name='download_activity_log'),

    path('store/<str:full_sap>/hr_indicators_report/', views.hr_indicators_report, name='hr_indicators_report'),
    path('store/<str:full_sap>/hr_indicators/', views.hr_indicators, name='hr_indicators'),

    path('store/<str:full_sap>/business_markdown/', views.business_markdown, name='business_markdown'),

    path('store/<str:full_sap>/business_write_offs/', views.business_write_offs, name='business_write_offs'),

    path('store/<str:full_sap>/business_rto/', views.business_rto, name='business_rto'),

    path('store/<str:full_sap>/scales/', views.scales, name='scales'),

    path('store/<str:full_sap>/poses/', views.poses, name='poses'),

    path('store/<str:full_sap>/kso/', views.kso, name='kso'),

    path('store/<str:full_sap>/services_net/', views.services_net, name='services_net'),

    path('store/<str:full_sap>/business_revenue/', views.business_revenue, name='business_revenue'),

    path('store/<str:full_sap>/services_alcohol/', views.services_alcohol, name='services_alcohol'),

    path('store/<str:full_sap>/services_loyalty/', views.services_loyalty, name='services_loyalty'),

    path('store/<str:full_sap>/services_cashless/', views.services_cashless, name='services_cashless'),

    path('upload/', views.upload_index, name='upload_index'),

    path('upload/file/', views.upload, name='upload'),

    path('upload/download/', views.hr_indicators_original, name='hr_indicators_original'),

    path('logout/', views.do_logout, name='logout'),

    path('store/<str:full_sap>/', views.dashboard, name='dashboard'),

    path('', views.index, name='index'),
]

