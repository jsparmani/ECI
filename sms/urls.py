from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path
from .import views

app_name = 'sms'


urlpatterns = [
    path('send/<str:complaint_type>/<int:msg_type>/<slug:name>/<int:phone_num>/<int:pk>/', views.send, name='send'),
    path('send_otp/<int:pk>/', views.send_otp, name='send_otp'),
    

]
