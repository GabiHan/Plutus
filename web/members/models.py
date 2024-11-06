from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class MemberManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError("The Login field must be set")
        user = self.model(login=login, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Create a superuser
        return self.create_user(login, password, **extra_fields)


class Member(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(max_length=25, unique=True)
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    age = models.PositiveIntegerField()
    
    # Required fields for Django authentication
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Can access the admin site
    is_superuser = models.BooleanField(default=False)  # Superuser status

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'age'] 

    objects = MemberManager()  # Use the custom manager

    def __str__(self):
        return self.login  

#Foreign key table for user personal account
class UserProfile(models.Model):
    user = models.OneToOneField(Member, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(default='default.jpg', upload_to='profile_images', null=True)

#define a new table, a foreign key of UserProfile that take care of the user input for his wallet 
class finance(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='financial_entries')
    money = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField()
    date = models.DateField()
    

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname}"
        return f"{self.comment} - {self.money} on {self.date}"


@receiver(post_save, sender=Member)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=Member)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
