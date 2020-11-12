from django.urls import path, include, re_path
from .views_password import pass_change, password, set_view, set_view_confirm, set_view_done
from myapp import views , views_appointment , views_prescription, views_message, views_profile, views_health, views_pdf

urlpatterns = [
    path('appointment/create/', views_appointment.appointment_create,name='appointment_create'),
    path('appointment/list/', views_appointment.appointment_list,name='appointment_list'),
    path('appointment/cancel/<int:pk>', views_appointment.appointment_cancel,name='appointment_cancel'),
    path('appointment/view/<int:pk>', views_appointment.appointment_view,name='appointment_view'),
    path('appointment/update/', views_appointment.update_view, name='update_view'),
    path('appointment/active/list/', views_appointment.active_list, name='active_list'),
    path('appointment/activation/<int:pk>', views_appointment.activation,name='active_view'),
    path('pres/create/', views_prescription.pres_create, name='pres_create'),
    path('pres/list/', views_prescription.pres_list, name='pres_list'),
    path('pres/view/<int:pk>', views_prescription.pres_view, name='pres_view'),
    path('pres/cancel/<int:pk>', views_prescription.pres_cancel, name='pres_cancel'),

    path('message/send/', views_message.msg_send, name='msg_sender'),
    path('message/receive/', views_message.msg_receive, name='msg_receive'),
    path('message/messenger/<ck>', views_message.messenger, name='messenger'),
    re_path('download/(?P<file_path>.*)/', views_message.file_response_download, name='file_download'),
    path('recent/', views_message.recent_msg, name='msg'),

    path('user/login/', views.login_view, name='loginview'),
    path('user/logout/', views.logout_view, name='logoutview'),
    path('user/register/', views.register, name='register'),
    path('user/profile/', views_profile.user_profile, name='profile'),
    path('user/profile/update/', views_profile.update_view, name='edit_profile'),
    path('user/profile/update/pic/', views_profile.update_pic, name='edit_pic'),

    path('user/profile/qualification/create/', views_health.qualification_create, name='qualification_create'),
    path('user/profile/qualification/view/', views_health.qualification_view, name='qualification_view'),
    path('user/profile/qualification/update/', views_health.qualification_update, name='qualification_update'),

    path('user/simple/profile/', views_health.simple_profile, name='simple_profile'),

    path('user/profile/health/create/', views_health.health_create, name='health_create'),
    path('user/profile/health/view/', views_health.health_view, name='health_view'),
    path('user/profile/health/update/', views_health.health_update, name='health_update'),
    path('user/profile/health/t_report/', views_health.t_report, name='t_report'),
    path('user/profile/health/t_report/cancel/', views_health.t_report_cancel, name='t_report_cancel'),

    path('mail/', views.mail, name='mail'),
    path('csv/', views.getfile, name='csv'),
    path('hello/<int:pk>/', views_pdf.HelloPDFView.as_view()),

    path('password/', password, name='password'),
    path('password/change/', pass_change, name='password_change'),
    path('set/view/', set_view, name='set_view'),
    path('set/view/confirm/', set_view_confirm, name='set_view_confirm'),
    path('set/view/done/', set_view_done, name='set_view_confirm'),

    path('user/search/', views.search_view, name='search_view'),
    path('user/', views.practice, name=''),

    path('pdf_view/', views_pdf.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views_pdf.DownloadPDF.as_view(), name="pdf_download"),
]
