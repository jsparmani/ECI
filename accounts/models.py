from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth

# Create your models here.


 



class Voter(models.Model):
    user = models.OneToOneField(
        User, related_name="voter_details", on_delete=models.CASCADE)
    phone_num = models.PositiveIntegerField()
    cons_no = models.PositiveIntegerField(blank=False)
    booth_no = models.PositiveIntegerField(blank=False)

    def __str__(self):
        return self.user.username

    def username(self):
        return self.user.username

    


class Constituency(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    booth = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id) 


class ComplaintType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class GovUser(models.Model):
    user = models.OneToOneField(User, related_name="gov", on_delete=models.CASCADE)
    is_supergov = models.BooleanField(default=False)
    phone_num = models.PositiveIntegerField()
    

    def __str__(self):
        return self.user.username

    def username(self):
        return self.user.username

class TempUser(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    phone_num = models.PositiveIntegerField()
    otp = models.PositiveIntegerField()
    send_time = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.username} {self.otp}'
