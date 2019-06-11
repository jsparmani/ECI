from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .import models
from .import forms
from accounts import models as acc_models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
import json
User = get_user_model()

def CheckBadWords(list2):
    list3=[]
    for item2 in list2:
        list3.append(f'{item2}\n'.lower())

    list1=open("D:/Codes/Django/filecomplaint/complaints/bad_words.txt",'r').readlines()
    for item1 in list3:
        for item2 in list1:
            if(item1==item2):
                return False
    return True



@login_required
def CreateComplaint(request):
    if request.method == 'POST':
        form = forms.ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                list2=str(form.cleaned_data['description']).split()
                res=CheckBadWords(list2)
                if not res:
                    return redirect('fault', fault=f'YOU CANNOT USE THESE OFFENSIVE WORD IN THE DESCRIPTION')
                complaint = form.save(commit=False)
                complaint.user = request.user
                complaint.save()
                pk=0
                return redirect('sms:send', complaint_type=slugify(complaint.choice), msg_type=2, name=complaint.user.username, phone_num = complaint.user.voter_details.phone_num, pk=pk)
            except:
                return redirect('fault', fault ="The record for this complaint already exists and is under progress")

        else:
            return redirect('fault', fault ="Something went wrong try again")
    else:
        form = forms.ComplaintForm()
    return render(request, 'complaint/complaint_form.html', {'form': form})

# All Data Display for the country


def allConstStatus(request):
    type_dict = acc_models.ComplaintType.objects.all().values('type')
    type_list = [u['type'] for u in type_dict]
    type_count = []

    dict = {}
    for type in type_list:
        num = models.Complaint.objects.all().filter(choice__iexact=type).count()
        dict[type] = num
        type_count.append(num)

    # Data for charts
    data = {
        "label": type_list,
        "value": type_count

    }
    jsondata = json.dumps(data)
    return render(request, 'complaint/display_all_stats.html', {'jsondata': jsondata, 'dict': dict})


# Get The Constitunecy number to display stats


def get_const_num(request):
    if request.method == 'POST':
        form = forms.get_number(request.POST)
        if form.is_valid():
            const = form.cleaned_data['const']
            const_list = [u['id']
                          for u in acc_models.Constituency.objects.all().values('id')]

            if not const in const_list:
                data = {
                    'const': [const],
                }
                jsondata = json.dumps(data)
                form = forms.get_number()
                return render(request, 'complaint/get_constituency.html', {'form': form, 'jsondata': jsondata})

            return redirect('complaints:display_const_stats', const=const)
        # const = request.POST['const']
    else:
        form = forms.get_number()
    return render(request, 'complaint/get_constituency.html', {'form': form})


# Get The type of complaint to display stats


def get_type(request):
    if request.method == 'POST':
        form = forms.get_type_form(request.POST)
        if form.is_valid():
            type = form.cleaned_data['type']
            type = slugify(type)
            return redirect('complaints:display_type_stats', type=type)
        # const = request.POST['const']
    else:
        form = forms.get_type_form()
    return render(request, 'complaint/get_complaint_type.html', {'form': form})


def get_type_num(request):
    if request.method == 'POST':
        form = forms.get_type_num_form(request.POST)
        if form.is_valid():
            type = form.cleaned_data['type']
            type = slugify(type)
            const = form.cleaned_data['const']
            select_all = form.cleaned_data['select_all']
            select_all = int(select_all)
            const_list = [u['id']
                          for u in acc_models.Constituency.objects.all().values('id')]
            if not const in const_list and not select_all:
                data = {
                    'const': [const],
                }
                jsondata = json.dumps(data)
                form = forms.get_type_num_form()
                return render(request, 'complaint/get_complaint_type_num.html', {'form': form, 'jsondata': jsondata})
            return redirect('complaints:complaint_list', type=type, const=const, select_all=select_all)
        # const = request.POST['const']
    else:
        form = forms.get_type_num_form()
    return render(request, 'complaint/get_complaint_type_num.html', {'form': form})


# Display stats of a particular constituency


def display_const_stats(request, const):
    type_dict = acc_models.ComplaintType.objects.all().values('type')
    type_list = [u['type'] for u in type_dict]
    type_count = []

    dict = {}
    for type in type_list:
        num = models.Complaint.objects.all().filter(
            choice__iexact=type, user__voter_details__cons_no__iexact=const).count()
        dict[type] = num
        type_count.append(num)
    data = {
        "label": type_list,
        "value": type_count

    }

    jsondata = json.dumps(data)
    return render(request, 'complaint/display_const_stats.html', {'jsondata': jsondata, 'dict': dict, 'const': const})


#  Display stats of a particular type


def display_type_stats(request, type):
    dict = {}
    const_list = []
    num_list = []
    id_list = [u['id'] for u in acc_models.Constituency.objects.all().values('id')]
    type = type.replace("-", " ")
    if type!='all':
        for id in id_list:
            num = models.Complaint.objects.all().filter(
                choice__iexact=type, user__voter_details__cons_no__iexact=id).count()
            dict.update({id: num})
            const_list.append(str(id))
            num_list.append(num)
    else:
        for id in id_list:
            num = models.Complaint.objects.all().filter(user__voter_details__cons_no__iexact=id).count()
            dict.update({id: num})
            const_list.append(str(id))
            num_list.append(num)
    data = {
        "label": const_list,
        "value": num_list

    }
    jsondata = json.dumps(data)
    return render(request, 'complaint/display_type_stats.html', {'dict': dict, 'jsondata': jsondata, 'type': type})
# Updating viewed boolean value


@login_required
def update_view(request, pk):
    present_complaint = models.Complaint.objects.get(pk=pk)
    if present_complaint.viewed_complaint == False:
        present_complaint.viewed_complaint = True
        present_complaint.save()
        return redirect('sms:send',complaint_type=(present_complaint.choice), msg_type=3, name=present_complaint.user.username, phone_num=present_complaint.user.voter_details.phone_num, pk=pk)
    else:
        return redirect('complaints:single', pk=pk)

# Display stats for govt


class ComplaintList(generic.ListView, LoginRequiredMixin):
    model = models.Complaint
    template_name = 'complaint/complaint_list.html'

    def get_queryset(self):
        
        queryset = super().get_queryset()
        type_new = self.kwargs.get("type").replace("-", " ")
        select_all = self.kwargs.get("select_all")
        
        if type_new == 'all' and select_all == 0:
            return queryset.filter(user__voter_details__cons_no__iexact=self.kwargs.get("const"))

        if type_new == 'all' and select_all == 1:
            return queryset

        if type_new != 'all' and select_all == 1:
            return queryset.filter(choice__iexact=type_new)

        return queryset.filter(choice__iexact=type_new, user__voter_details__cons_no__iexact=self.kwargs.get("const"))

# Display stat for particular complaint


class ComplaintDetail(generic.DetailView, LoginRequiredMixin):
    model = models.Complaint
    template_name = 'complaint/complaint_detail.html'


class UserComplaints(LoginRequiredMixin, generic.ListView):
    model = models.Complaint
    template_name = "complaint/user_complaint_list.html"

    def get_queryset(self):
        try:
            self.complaint_user = User.objects.prefetch_related(
                "complaints").get(username__iexact=self.kwargs.get("username"))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.complaint_user.complaints.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["complaint_user"] = self.complaint_user
        return context


@login_required
def add_comment_to_complaint(request, pk):
    complaint = get_object_or_404(models.Complaint, pk=pk)

    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.complaint = complaint
            comment.save()
            return redirect('sms:send',complaint_type=slugify(complaint.choice), msg_type=4, name=complaint.user.username, phone_num=complaint.user.voter_details.phone_num, pk=complaint.pk)

    else:
        form = forms.CommentForm()
    return render(request, 'complaint/comment_form.html', {'form': form})





@login_required
def likes(request,pk):
    complaint = models.Complaint.objects.get(pk__iexact = pk)
    if complaint.is_liked == True:
        complaint.is_liked = False
        complaint.save()
    elif complaint.is_liked == False:
        complaint.is_liked = True
        complaint.is_disliked = False
        complaint.save()
    return redirect('complaints:single', pk=pk)


@login_required
def dislikes(request,pk):
    complaint = models.Complaint.objects.get(pk__iexact = pk)
    if complaint.is_disliked == True:
        complaint.is_disliked = False
        complaint.save()
    elif complaint.is_disliked == False:
        complaint.is_disliked = True
        complaint.is_liked = False
        complaint.save()
    return redirect('complaints:single', pk=pk)    