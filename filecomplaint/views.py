from django.shortcuts import render
from django.views.generic import TemplateView
from accounts import models as acc_models
from complaints import models as com_models
from django.contrib.auth.models import User
import json


class HomePage(TemplateView):
    template_name = 'index.html'

    def get(self, request):
        likes = com_models.Complaint.objects.all().filter(is_liked__iexact=1).count()
        dislikes = com_models.Complaint.objects.all().filter(is_disliked__iexact=1).count()
        total_complaints = com_models.Complaint.objects.all().count()
        viewed_complaints = com_models.Complaint.objects.all().filter(viewed_complaint__iexact=1).count()
        cons_list = [u['id'] for u in acc_models.Constituency.objects.all().values('id')]
        max_id = [-1]
        max_complaints = -1
        for cons in cons_list:
            complaints_num = com_models.Complaint.objects.all().filter(user__voter_details__cons_no__iexact=cons).count()
            if complaints_num>max_complaints:
                max_complaints=complaints_num
                max_id=[]
                max_id.append(cons)
            elif complaints_num == max_complaints:
                max_id.append(cons)
        data={
            'polls':[likes,dislikes]

        }
        jsondata = json.dumps(data)
        return render(request, self.template_name, {'likes':likes, 'dislikes':dislikes, 'total_complaints':total_complaints, 'viewed_complaints':viewed_complaints, 'jsondata':jsondata, 'max_complaints':max_complaints, 'max_id':max_id})

class WelcomePage(TemplateView):
    template_name = 'welcome.html'


class ThanksPage(TemplateView):
    template_name = 'thanks.html'

def fault_page(request,fault):
    return render(request, 'fault.html', {'fault':fault})


