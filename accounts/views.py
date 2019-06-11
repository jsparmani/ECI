from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from .import forms
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.models import User
import json
from django.core.exceptions import ValidationError
from .import models
from random import randint
import datetime
# Create your views here.



def TempLogin(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            tuser = authenticate(request, username=username, password=password)
            id_list = [u['user'] for u in models.GovUser.objects.all().values('user')]
            govname_list=[]
            for num in id_list:
                temp = User.objects.get(id__iexact = num)
                temp_name = temp.username
                govname_list.append(temp_name)
            

            if tuser is not None:
                if username in govname_list:
                    user1 = models.GovUser.objects.get(user__username__iexact=username)
                    phone_num=user1.phone_num
                else:
                    user1 = models.Voter.objects.get(user__username__iexact=username)
                    phone_num = user1.phone_num
                otp = randint(100000, 999999)
                temp_user = models.TempUser.objects.create(username=username, password=password, phone_num=phone_num, otp = otp)
                return redirect('sms:send_otp', pk=temp_user.pk)
            else:
                return redirect('fault',fault="Invalid Credentials. Please Try Again.")
    else:
        form = forms.LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def login(request, pk):
    temp_user = models.TempUser.objects.get(pk=pk)
    if request.method == 'POST':
        form = forms.OtpForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            
            if otp==temp_user.otp:
                user = authenticate(request,username=temp_user.username, password=temp_user.password)
                t1 = f'{str(temp_user.send_time)[11:13:]}:{str(temp_user.send_time)[14:16:]}:{str(temp_user.send_time)[17:19:]}'
                
                t2 = f'{str(datetime.datetime.now().hour)}:{str(datetime.datetime.now().minute)}:{str(datetime.datetime.now().second)}'
                
                FMT = '%H:%M:%S'
                diff = datetime.datetime.strptime(t2, FMT) - datetime.datetime.strptime(t1,FMT)
                
                if diff.total_seconds() < 600:
                    auth_login(request, user)
                    models.TempUser.objects.get(pk=pk).delete()
                    return redirect('home')
                else:
                    models.TempUser.objects.get(pk=pk).delete()
                    return redirect('fault',fault="Time Limit Exceeded. Please Try Again.")
            else:
                models.TempUser.objects.get(pk=pk).delete()
                return redirect('fault',fault="Invalid OTP. Please Try Again.")
    else:
        form = forms.OtpForm()
        try:
            pno = models.Voter.objects.get(user__username__iexact = temp_user.username).phone_num
        except:
            pno = models.GovUser.objects.get(user__username__iexact = temp_user.username).phone_num
        tpno=str(pno)
        phone_num = f'******{tpno[6:10:]}'
    return render(request, 'accounts/otp_form.html', {'form': form, 'pk':pk, 'phone_num':phone_num})


def add_user(request):
    if request.method == 'POST':
        form = forms.AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                temp = User.objects.get(username=username)
            except:
                user = User.objects.create_user(username, '', password)
                user.save()
                return redirect('accounts:add_voter', username=username)
        data = {
            'username': ['username']
        }
        jsondata = json.dumps(data)
        form = forms.AddUserForm()
        return render(request, 'accounts/add_user.html', {'form': form, 'jsondata': jsondata})
    else:
        form = forms.AddUserForm()
        return render(request, 'accounts/add_user.html', {'form': form})


def add_voter(request, username):
    if request.method == 'POST':
        form = forms.AddVoterForm(request.POST)
        if form.is_valid():
            voter = form.save(commit=False)
            voter.user = User.objects.get(username=username)
            voter.save()
            form = forms.AddUserForm()
            return redirect('accounts:add_user')

    else:
        form = forms.AddVoterForm()
        return render(request, 'accounts/add_voter.html', {'form': form, 'username': username})


def add_gov_user(request):
    if request.method == 'POST':
        form = forms.AddGovUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                temp = User.objects.get(username=username)
            except:
                user = User.objects.create_user(username, email , password)
                user.save()
                return redirect('accounts:add_gov_user_phone', username=username)

        data = {
            'username': ['username']
        }
        jsondata = json.dumps(data)
        form = forms.AddGovUserForm()
        return render(request, 'accounts/add_gov_user.html', {'form': form, 'jsondata': jsondata})
    else:
        form = forms.AddGovUserForm()
    return render(request, 'accounts/add_gov_user.html', {'form': form})


def add_gov_user_phone(request, username):
    if request.method == 'POST':
        form = forms.AddGovPhoneForm(request.POST)
        if form.is_valid():
            gov = form.save(commit=False)
            gov.user = User.objects.get(username=username)
            gov.save()
            form = forms.AddUserForm()
            return redirect('accounts:add_gov_user')

    else:
        form = forms.AddGovPhoneForm()
        return render(request, 'accounts/add_gov_user_phone.html', {'form': form, 'username': username})


def add_constituency(request):
    if request.method == 'POST':
        form = forms.ConstituencyForm(request.POST)
        if form.is_valid():
            const = form.save()
            data = {'id':form.cleaned_data['id']+1}
            form = forms.ConstituencyForm(initial = data)
            return render(request, 'accounts/add_constituency.html',{'form':form})
        else:
            return redirect('fault', fault="Constituency with this ID already exists")
            
    else:
        form = forms.ConstituencyForm()
        return render(request, 'accounts/add_constituency.html',{'form':form}) 


def update_constituency(request):
    if request.method == 'POST':
        form = forms.UpdateConstituencyForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            booth = form.cleaned_data['booth']
            temp_cons = models.Constituency.objects.all().filter(id__iexact = id)
            if temp_cons.exists():
                temp_cons = models.Constituency.objects.get(id__iexact = id)
                temp_cons.booth = booth
                temp_cons.save()
                return redirect('home')
            else:
                return redirect('fault', fault = 'This Constituency ID does NOT exists')
        else:
            return redirect('fault', fault = 'Something went wrong. Try Again.')
    else:
        form = forms.UpdateConstituencyForm()
        return render(request, 'accounts/constituency_update_form.html',{'form':form}) 


class ConstituencyList(generic.ListView):
    model = models.Constituency
    template_name = "accounts/constituency_list.html"


def add_complaint_type(request):
    if request.method == 'POST':
        form = forms.ComplaintTypeForm(request.POST)
        if form.is_valid():
            complaint_type = form.save()
            form = forms.ComplaintTypeForm()
            return render(request, 'accounts/add_complaint_type.html',{'form':form})
        else:
            return redirect('fault', fault="Complaint of this type already exists")
            
    else:
        form = forms.ComplaintTypeForm()
        return render(request, 'accounts/add_complaint_type.html',{'form':form})