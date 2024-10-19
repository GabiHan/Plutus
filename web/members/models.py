# Create our database models here. By default, django already has SQL tables all set up
#All we need to do is define items. Do py manage.py migrate to execute the table 


from django.db import models
#from django.contrib.auth.models import User
from datetime import date

class Member(models.Model):
    login = models.CharField(max_length=255, unique=True, default="Morose")
    password = models.CharField(max_length=255, default="Hello123")  
    firstname = models.CharField(max_length=255, default="Mor")
    lastname = models.CharField(max_length=255, default="Morse")

#Default values are set in age and birth to avoid the "non-nullable" error"
    age = models.PositiveIntegerField(default=18)
    birth = models.DateField(default=date(2000, 1, 1))  

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

