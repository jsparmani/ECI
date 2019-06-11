from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts import models as acc_models
import requests


def send(request, complaint_type, msg_type, name, phone_num, pk):
    complaint_type.replace("-", " ")
    return HttpResponse("WORKING")
    # api_key = '292a8d1f-295e-11e9-9ee8-0200cd936042'
    # if(msg_type == 2):
    #     template_name = 'Complaint Registration'
    #     link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey={api_key}&to={phone_num}&from=ECIWEB&templatename={template_name}&var1={name}&var2={complaint_type}'
    #     requests.get(link)
    #     return redirect('home')
    # elif(msg_type == 3):
    #     template_name = 'Complained Viewed'
    #     link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey={api_key}&to={phone_num}&from=ECIWEB&templatename={template_name}&var1={name}&var2={complaint_type}'
    #     requests.get(link)
    #     return redirect('complaints:single', pk=pk)
    # elif(msg_type == 4):
    #     template_name = 'Complaint Comment'
    #     link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey={api_key}&to={phone_num}&from=ECIWEB&templatename={template_name}&var1={name}&var2={complaint_type}'
    #     requests.get(link)
    #     return redirect('complaints:single', pk=pk)
        


def send_otp(request, pk):
    temp_user = acc_models.TempUser.objects.get(pk=pk)
    phone_num = temp_user.phone_num
    otp = temp_user.otp
    username = temp_user.username
    api_key = '292a8d1f-295e-11e9-9ee8-0200cd936042'
    msg_type = 1
    template_name = 'OTP'
    print(otp)
    # link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey={api_key}&to={phone_num}&from=ECIWEB&templatename={template_name}&var1={username}&var2={otp}'
    # requests.get(link)
    # return HttpResponse(f'{temp_user.username} {temp_user.phone_num} {temp_user.otp}')
    return redirect('accounts:permanent_login', pk=pk)

    


    

    



    


