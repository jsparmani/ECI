from django.contrib import admin
from .import models

# Register your models here.

class ConstituencyAdmin(admin.ModelAdmin):
    list_display = ['id', 'booth']


class GovUserAdmin(admin.ModelAdmin):
    list_display = ['username','phone_num','is_supergov'] 
    list_filter = ['is_supergov']


class VoterAdmin(admin.ModelAdmin):
    list_display = ['username','cons_no', 'booth_no', 'phone_num']
    list_filter = ['cons_no']

admin.site.register(models.Voter, VoterAdmin)
admin.site.register(models.Constituency, ConstituencyAdmin)
admin.site.register(models.ComplaintType)
admin.site.register(models.GovUser, GovUserAdmin)
admin.site.register(models.TempUser)
