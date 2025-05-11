from django.contrib import admin
from .models import Visitors,Host,visit,Company,setting,print_tag

# Register your models here.
admin.site.register(Visitors)
admin.site.register(Host)
admin.site.register(visit)
admin.site.register(Company)
admin.site.register(setting)
admin.site.register(print_tag)
# @admin.register(Visitors())
# class profile(admin.ModelAdmin):
#     list_display = ['visitorId', 'firstname', 'fname', 'role', 'email']
