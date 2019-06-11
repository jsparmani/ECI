from django.contrib import admin
from .import models

# Register your models here.


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['choice', 'Constituency_number', 'Booth_number','created_at','viewed_complaint',]
    list_filter=['viewed_complaint']


admin.site.register(models.Complaint, ComplaintAdmin)
admin.site.register(models.Comment)

