from django.urls import path
from . import views


urlpatterns = [
    path('sign_in/', views.sign_in, name='sign_in'),
    path('store/<str:full_sap>/products_low_saled_report/', views.products_low_saled_report, name='products_low_saled_report'),
    path('store/<str:full_sap>/products_low_saled/', views.products_low_saled, name='products_low_saled'),

    path('store/<str:full_sap>/products_stoped_report/', views.products_stoped_report, name='products_stoped_report'),
    path('store/<str:full_sap>/products_stoped_food_report/', views.products_stoped_food_report, name='products_stoped_food_report'),
    path('store/<str:full_sap>/products_stoped_nonfood_report/', views.products_stoped_nonfood_report, name='products_stoped_nonfood_report'),
    path('store/<str:full_sap>/products_stoped_fresh_report/', views.products_stoped_fresh_report, name='products_stoped_fresh_report'),
    path('store/<str:full_sap>/products_stoped/', views.products_stoped, name='products_stoped'),
    path('store/<str:full_sap>/products_stoped_food/', views.products_stoped_food, name='products_stoped_food'),
    path('store/<str:full_sap>/products_stoped_nonfood/', views.products_stoped_nonfood, name='products_stoped_nonfood'),
    path('store/<str:full_sap>/products_stoped_fresh/', views.products_stoped_fresh, name='products_stoped_fresh'),

    path('store/<str:full_sap>/products_minus_report/', views.products_minus_report, name='products_minus_report'),
    path('store/<str:full_sap>/products_minus/', views.products_minus, name='products_minus'),

    path('store/<str:full_sap>/products_top30_today_report/', views.products_top30_today_report, name='products_top30_today_report'),
    path('store/<str:full_sap>/products_top30_week_report/', views.products_top30_week_report, name='products_top30_week_report'),
    path('store/<str:full_sap>/products_top30/', views.products_top30, name='products_top30'),

    path('store/<str:full_sap>/products_topvd_report/', views.products_topvd_report, name='products_topvd_report'),
    path('store/<str:full_sap>/products_topvd/', views.products_topvd, name='products_topvd'),

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

    path('store/<str:full_sap>/business_checks_traffic_report/', views.business_checks_traffic_report, name='business_checks_traffic_report'),
    path('store/<str:full_sap>/business_checks_traffic/', views.business_checks_traffic, name='business_checks_traffic'),

    path('store/<str:full_sap>/business_old_price_report/', views.business_old_price_report, name='business_old_price_report'),
    path('store/<str:full_sap>/business_old_price/', views.business_old_price, name='business_old_price'),

    path('store/<str:full_sap>/business_write_offs/', views.business_write_offs, name='business_write_offs'),

    path('store/<str:full_sap>/business_rto/', views.business_rto, name='business_rto'),

    path('store/<str:full_sap>/scales/', views.scales, name='scales'),

    path('store/<str:full_sap>/poses/', views.poses, name='poses'),

    path('store/<str:full_sap>/kso/', views.kso, name='kso'),

    path('store/<str:full_sap>/services_net/', views.services_net, name='services_net'),

    path('store/<str:full_sap>/business_revenue_new_report/', views.business_revenue_new_report, name='business_revenue_new_report'),
    path('store/<str:full_sap>/business_revenue_new/', views.business_revenue_new, name='business_revenue_new'),

    path('store/<str:full_sap>/services_alcohol/', views.services_alcohol, name='services_alcohol'),

    path('store/<str:full_sap>/services_loyalty/', views.services_loyalty, name='services_loyalty'),

    path('store/<str:full_sap>/services_cashless/', views.services_cashless, name='services_cashless'),

    path('heatmap_page/', views.heatmap_page, name='heatmap_page'),

    path('get_heatmap/', views.get_heatmap, name='get_heatmap'),

    path('get_feedback/', views.get_feedback, name='get_feedback'),

    path('feedback/', views.feedback, name='feedback'),

    path('download_feedback/', views.download_feedback, name='download_feedback'),

    path('upload/', views.upload_index, name='upload_index'),

    path('upload/file/', views.upload, name='upload'),

    path('upload/download/', views.hr_indicators_original, name='hr_indicators_original'),

    path('logout/', views.do_logout, name='logout'),

    path('store/<str:full_sap>/', views.dashboard, name='dashboard'),

    path('store/<str:full_sap>/sap_name/', views.sap_name, name='sap_name'),
    
    path('store/<str:full_sap>/go_back/', views.go_back, name='go_back'),

    path('', views.index, name='index'),
]

