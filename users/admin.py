from django.contrib import admin
from .models import profile
# Register your models here.


@admin.register(profile)
class profile(admin.ModelAdmin):
    list_display = ['user_id', 'user', 'fname', 'role', 'email', 'is_online']
