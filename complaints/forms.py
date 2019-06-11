from django import forms
from .import models
from accounts import models as acc_models


class ComplaintForm(forms.ModelForm):

    class Meta():
        model = models.Complaint
        exclude = ['user', 'created_at', 'viewed_complaint', 'is_liked', 'is_disliked']
        widgets = {
            'choice': forms.Select(attrs = {'class': 'form-control mt-3', 'autofocus':'autofocus'}),
            'description': forms.Textarea(attrs = {'class': 'form-control', 'name': 'editor1'}),
            'file_upload': forms.FileInput(attrs = {'class': 'custom-file-input mt-3', 'type':'file', 'id':'image'}),
            'file_upload1': forms.FileInput(attrs = {'class': 'custom-file-input mt-3', 'type':'file', 'id':'image1'}),
            'file_upload2': forms.FileInput(attrs = {'class': 'custom-file-input mt-3', 'type':'file', 'id':'image2'}),
            'file_upload3': forms.FileInput(attrs = {'class': 'custom-file-input mt-3', 'type':'file', 'id':'image3'}),
            'file_upload4': forms.FileInput(attrs = {'class': 'custom-file-input mt-3', 'type':'file', 'id':'image4'}),
            'file_upload5': forms.FileInput(attrs = {'class': 'custom-file-input mt-3', 'type':'file', 'id':'image5'}),
        }


class get_number(forms.Form):

    const = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'autofocus':'autofocus'}))


class get_type_form(forms.Form):

    COMPLAINT_CHOICES = [('All','All')]
    type_list = [u['type']
                 for u in acc_models.ComplaintType.objects.all().values('type')]
    for temp in type_list:
        COMPLAINT_CHOICES.append((temp, temp))

    type = forms.ChoiceField(choices=COMPLAINT_CHOICES, widget=forms.Select(attrs={'class':'form-control', 'autofocus':'autofocus'}))


class get_type_num_form(forms.Form):

    const = forms.IntegerField(initial=0, widget=forms.NumberInput(attrs={'class':'form-control', 'autofocus':'autofocus'}))

    select_all = forms.BooleanField(required=False, widget = forms.CheckboxInput)

    COMPLAINT_CHOICES = [('All', 'All')]
    type_list = [u['type']
                 for u in acc_models.ComplaintType.objects.all().values('type')]
    for temp in type_list:
        COMPLAINT_CHOICES.append((temp, temp))

    type = forms.ChoiceField(choices=COMPLAINT_CHOICES, widget=forms.Select(attrs={'class':'form-control'}))


class CommentForm(forms.ModelForm):

    class Meta():
        model = models.Comment
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows':3, 'autofocus':'autofocus'})
        }


