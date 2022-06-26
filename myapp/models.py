from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Document(models.Model):
  user = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)                      
  DocumentSrNo= models.IntegerField(null=True)

  DocumentName = models.CharField(max_length=50, null=True)
 


  Remarks = models.TextField(null=True)
  file = models.FileField(null=True)