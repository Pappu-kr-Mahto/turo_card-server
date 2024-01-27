from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class TuroCards(models.Model):
    Card_visibility = [
        ('public','public'),
        ('private','private')
    ]
    user_id=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    username=models.CharField(max_length=100,default="")
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="images",null=True)
    description=models.TextField()
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.IntegerField(null=True)
    card_no=models.IntegerField()
    status=models.CharField(max_length=20,choices=Card_visibility)
    likes=models.TextField('[]',default=[])
    likes_count=models.IntegerField(default=0)
    comments=models.TextField('[]',default=[])

class SwappingRequest(models.Model):        
        senderUser=models.CharField(max_length=100)
        receiverUser=models.CharField(max_length=100)
        senderCard=models.IntegerField(null=False,default=0)
        receiverCard=models.IntegerField(null=False,default=0)

