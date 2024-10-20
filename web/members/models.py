# Create our database models here. By default, django already has SQL tables all set up
#All we need to do is define items. Do py manage.py migrate to execute the table 


from django.db import models
#from django.contrib.auth.models import User
from datetime import date

class Member(models.Model):
    login = models.CharField(max_length=25, unique=True, default="login")
    password = models.CharField(max_length=25, default="0")  
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    age = models.PositiveIntegerField()
    birth = models.DateField()  

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class account(models.Model):
    id_money = models.ForeignKey(Member, on_delete = models.CASCADE)
    add_money = models.CharField(max_length=255)
    date = models.DateField()
