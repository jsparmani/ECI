from .import models as acc_models
from django.contrib.auth.models import User

def GovList(request):
    id_list = [u['user'] for u in acc_models.GovUser.objects.all().values('user')]
    govname_list=[]
    for num in id_list:
        temp = User.objects.get(id__iexact = num)
        temp_name = temp.username
        govname_list.append(temp_name)

    return {'govname_list':govname_list}