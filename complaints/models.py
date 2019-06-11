from django.urls import reverse
from django.db import models
from accounts import models as acc_models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


class Complaint(models.Model):

    user = models.ForeignKey(
        User, related_name='complaints', on_delete=models.CASCADE)
    

    COMPLAINT_CHOICES = []
    type_list = [u['type'] for u in acc_models.ComplaintType.objects.all().values('type')]
    for temp in type_list:
        COMPLAINT_CHOICES.append((temp,temp))

    choice = models.CharField(
        max_length=50, choices=COMPLAINT_CHOICES, blank=False)
    description = models.TextField(blank=True)
    file_upload = models.FileField(
        upload_to='files/', blank=True)
    file_upload1 = models.FileField(
        upload_to='files/', blank=True)
    file_upload2 = models.FileField(
        upload_to='files/', blank=True)
    file_upload3 = models.FileField(
        upload_to='files/', blank=True)
    file_upload4 = models.FileField(
        upload_to='files/', blank=True)
    file_upload5 = models.FileField(
        upload_to='files/', blank=True)

    created_at = models.DateTimeField(auto_now=True)

    viewed_complaint = models.BooleanField(default=False)

    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)

    def __str__(self):
        return self.choice

    def get_absolute_url(self):
        return reverse('home')

    def Constituency_number(self):
        return self.user.voter_details.cons_no
    
    def Booth_number(self):
        return self.user.voter_details.booth_no

    class Meta():
        ordering = ['created_at']
        unique_together = ["user", "choice"]


        
        #model Comment
class Comment(models.Model):
    complaint = models.ForeignKey(
        'complaints.Complaint', related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('complaints:single', kwargs={'pk': self.pk})

    def __str__(self):
        return self.text
