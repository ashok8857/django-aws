from django import forms
from .models import *
from django.contrib.auth.models import User



class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['DocumentSrNo','DocumentName','Remarks','file'] #'user',
        # widgets ={
        #     'user':forms.HiddenInput()
        # }   
