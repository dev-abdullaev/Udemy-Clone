from urllib import request
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver



class CustomUser(AbstractUser):
    profile_picture = models.ImageField(default="default_pic.png", upload_to='users/')
    is_active = models.BooleanField(default=False)


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    

    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'




def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        if instance.is_active == False:
            Teacher.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=CustomUser)