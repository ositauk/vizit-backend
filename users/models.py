from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone


# Profile Model
class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    role = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    fname = models.CharField(max_length=100, null=True)
    is_online = models.BooleanField(default=False)
    forget_password_token = models.CharField(max_length=100, null=True)
    login_time = models.TimeField(null=True)
    logout_time = models.TimeField(null=True)


# Create signal for deletion of user if profile is delete
@receiver(post_delete, sender=profile)
def delete_user(sender, instance, **kwargs):
    print("User Deleted")
    instance.user.delete()

