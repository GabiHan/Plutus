"""from django.urls import path, include
from django.contrib import admin
from members import views as members_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('home.urls')),
    #path('register/', members_views.Register, name ='register'),
    #path('members/', include('members.urls')), 
    
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.members, name='members-home'),  # This handles /members/
    path('register/', views.Register, name='register'),  # This handles /members/register/
]
"""
from django.urls import path
from .views import register, login_view, user_profile

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login_view'),
    path('index/', user_profile, name='user_profile')

]
