
from distutils.command.upload import upload
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from .views import print_userReport,GetvisitorsDetails,deleteschedulevisit,GetHostDetails,cardPrint,home,checkin,checkout, upload_host,users,schedulevisit,seating,user_reports,user_to_blacklist,user_to_whitelist,show_visitors,visitor_whitelist,visitor_blacklist,takeimg,report_host,search_visitors,user_to_blank,weekly_report, monthly_report,visit,edit_settings,printtag_list,cardPrint_byPhone,cardPrint_delete,print_weeklyreport,print_monthlyreport,upload_host

urlpatterns = [
    path('',home,name='home'),
    path('checkin/',checkin,name='checkin'),
    path('checkin-conformation/',checkin,name='checkin'),
    path('checkout/',checkout,name='checkout'),

    path('getuserdetails/<int:hostid>',GetHostDetails,name='GetHostDetails'),
    path('getvisitorsdetails/<int:visitorid>',GetvisitorsDetails,name='GetvisitorsDetails'),
    
    path('schedulevisit/',schedulevisit,name='schedulevisit'),
    path('deleteschedulevisit/<int:id>',deleteschedulevisit,name='schedulevisit'),
    path('users/',users,name='users'),
    path('setting/',seating,name='seating'),
    path('edit_setting/',edit_settings,name='edit_setting'),
    path('report/',user_reports,name='report'),
    path('report_hosts/',report_host,name='report_hosts'),
    path('weekly_report/',weekly_report,name='weekly_report'),
    path('monthly_report/',monthly_report,name='monthly_report'),
    path('takeimg/',takeimg,name='takeimg'),
    path('show_visiter/', show_visitors, name='show_visiter'),
    path('search_visiter/', search_visitors, name='search_visiter'),
    path('blankentry/<int:id>', user_to_blank, name='user_to_blankentry'),
    path('blacklist/<int:id>', user_to_blacklist, name='user_to_blacklist'),
    path('whitelist/<int:id>', user_to_whitelist, name='user_to_whitelist'),
    path('visitor_whitelist/', visitor_whitelist, name='visiter_whitelist'),
    path('visitor_blacklist/', visitor_blacklist, name='visiter_blacklist'),
    path('visit/', visit, name='visit'),
    path('printtag_details/',printtag_list,name='printtag_details'),
    path('card_print/<int:id>', cardPrint_byPhone, name='card_print'),
    path('card_delete/<int:id>', cardPrint_delete, name='card_delete'),
    path('print_weekly/', print_weeklyreport, name='print_weekly'),
    path('print_monthly/', print_monthlyreport, name='print_monthly'),
    path('print_userReport/<value>/', print_userReport, name='print_userReport'),
    path('print_hostReport/<value>/', print_userReport, name='print_hostReport'),
    path('card/<int:id>', cardPrint), 
    path('upload/', upload_host, name='upload'),
]


