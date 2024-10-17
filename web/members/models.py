# Create our database models here. By default, django already has SQL tables all set up
#All we need to do is define items. Do py manage.py migrate to execute the table 


from django.db import models
from datetime import date

class Member(models.Model):
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)  
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)

#Default values are set in age and birth to avoid the "non-nullable" error"
    age = models.PositiveIntegerField(default=18)
    birth = models.DateField(default=date(2000, 1, 1))  


    def __str__(self):
        return f"{self.firstname} {self.lastname}"

