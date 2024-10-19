from django.contrib import admin
from .models import Member 

# Make members visible on the admin interface
admin.site.register(Member)
