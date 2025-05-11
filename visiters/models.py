from pyexpat import model
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime
import pytz

class Visitors(models.Model):
    visitorId=models.AutoField(primary_key=True)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100, null=True)
    address=models.CharField(max_length=100)
    Visitors_phone_number = PhoneNumberField()
    pourpose=models.CharField(max_length=100)
    blacklisted=models.IntegerField()
    imageurl=models.TextField(max_length=20000)
    visitor_company=models.CharField(max_length=100)

class Company(models.Model):
    companyName=models.CharField(max_length=100)
    companyLogo=models.ImageField()
    companyEmail=models.EmailField()

class Host(models.Model):
    hostname=models.CharField(max_length=50)
    Host_phone_number =models.CharField(max_length=20)
    department=models.CharField(max_length=50)

class visit(models.Model):
    visitors=models.ForeignKey(Visitors, on_delete=models.CASCADE)
    host=models.ForeignKey(Host, on_delete=models.CASCADE)
    checkInDate= models.DateField( blank=True,null=True)
    checkOutDate= models.DateField(null=True,blank=True)
    checkInTime=models.TimeField(blank=True,null=True)
    checkOutTime=models.TimeField(null=True, blank=True)
    user_name=models.CharField(max_length=30,blank=True)

    cheakedINinfo=models.IntegerField(null=True)

    schedukevisit=models.IntegerField(default=0)
    schedule_date=models.DateField(null=True,blank=True)
    schedule_time=models.TimeField(null=True, blank=True)
    schedule_pin=models.IntegerField(unique=True,null=True)
    def __str__(self):
        return str(self.checkInTime)

class print_tag(models.Model):
    visit_id = models.ForeignKey(visit, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50, null=True)
    checkin_Time=models.TimeField(blank=True, null=True)
    checkout_Date= models.DateField(blank=True, null=True)
    host_name=models.CharField(max_length=50, null=True)
    imageurl=models.TextField(max_length=10000)
    status = models.IntegerField(default=0)

class setting(models.Model):
    compLogo = models.ImageField(upload_to="images")
    compName = models.CharField(max_length=50)
    compEmail = models.CharField(max_length=50)

