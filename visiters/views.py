from datetime import datetime, timedelta
from importlib.metadata import files
import pytz
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import request
from . models import * 
import csv
# from .models import Company, Visitors,Host,visit,setting,print_tag
# import keyboard
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from random import randint
from django.contrib import messages
from django.http import JsonResponse

@login_required(login_url='/user/login/')
def home(request):
    count = visit.objects.filter(cheakedINinfo=1).count()
    CCount = visit.objects.filter(cheakedINinfo=2).count()
    Scount=visit.objects.filter(schedukevisit=1).count()
    host_details=Host.objects.all()
    visiters_details=Visitors.objects.all()
    username=request.user.username
    intz = pytz.timezone('Africa/Lagos')
    nowdt = datetime.now(intz)

    if request.method == 'POST':
        count = visit.objects.filter(cheakedINinfo=1).count()
        CCount = visit.objects.filter(cheakedINinfo=2).count()
        Scount=visit.objects.filter(schedukevisit=1).count()

        firstname = request.POST['firstname']
        phonenumber = request.POST['phonenumber']
        # print("the visitor details ====>",firstname,phonenumber)

        first = firstname
        if len(firstname)==1:
            lastname = 1
        else:
            lastname=firstname[1]

        hostname = request.POST['hostname']
        departmentname = request.POST.get('department',False)
        hostPhonenumber=request.POST['HostPhoneNumber']
        
        print("===host details",hostname,departmentname,hostPhonenumber)
        exist_visitor=visit.objects.filter(visitors__firstname=first,visitors__Visitors_phone_number=phonenumber).last()
        print("===visitor details ",exist_visitor)
        exist_host=Host.objects.filter(hostname=hostname,Host_phone_number=hostPhonenumber,department=departmentname)
        if not exist_host:
            messages.error(request, 'The host is not present in the dataBase !! please Add a new host')
            return HttpResponseRedirect("/?error=1")
            
        if exist_visitor.cheakedINinfo==1:
            messages.error(request, 'The visitor is already checked In !! please check out first ' )
            return HttpResponseRedirect("/?error=1")

        
        if exist_visitor.visitors.blacklisted==2:
            messages.error(request, 'This visitor is Blacklisted !!' )
            return HttpResponseRedirect("/?error=1")
            

        host_id=Host.objects.get(hostname=hostname,Host_phone_number=hostPhonenumber,department=departmentname)
        visitor_id=Visitors.objects.get(firstname=exist_visitor.visitors.firstname,Visitors_phone_number=phonenumber)
        checkInDetails=visit(host=host_id,visitors=visitor_id,user_name=username,cheakedINinfo=1,checkInTime=nowdt,checkInDate=nowdt)
        checkInDetails.save()
        return render(request, 'visiters/checkin-conformation-details.html', {'total': count, 'CCount': CCount,'scount':Scount,'details':checkInDetails})
    return render(request, 'visiters/dashbord.html', {'total': count, 'CCount': CCount,'scount':Scount,'host':host_details,'username':username,'visiters':visiters_details})


@login_required(login_url='/user/login/')
def GetHostDetails(request,hostid):
    hostData=Host.objects.get(id=hostid)
    print("==",hostData.department)
    print("==",hostData.Host_phone_number)
    response = {'hostname':hostData.hostname,'department':hostData.department, 'phoneNumber':str(hostData.Host_phone_number)}
    return JsonResponse(response, safe=False)

def GetvisitorsDetails(request,visitorid):
    visitorsdata=Visitors.objects.get(visitorId=visitorid)
    print("==",visitorsdata.firstname)
    print("==",visitorsdata.Visitors_phone_number)
    response = {'firstname':visitorsdata.firstname,'lastname':visitorsdata.lastname, 'phoneNumber':str(visitorsdata.Visitors_phone_number),'imageurl':visitorsdata.imageurl}
    return JsonResponse(response, safe=False)

@login_required(login_url='/user/login/')
def checkin(request):
    count = visit.objects.filter(cheakedINinfo=1).count()
    CCount = visit.objects.filter(cheakedINinfo=2).count()
    Scount=visit.objects.filter(schedukevisit=1).count()
    host_details=Host.objects.all()
    visiters_details=Visitors.objects.all()

    username=request.user.username
    if request.method == 'POST':
        print(request.POST)
        count = visit.objects.filter(cheakedINinfo=1).count()
        CCount = visit.objects.filter(cheakedINinfo=2).count()
        Scount=visit.objects.filter(schedukevisit=1).count()
        firstname = request.POST['firstname'].lower()
        lastname = request.POST['lastname'].lower()
        compname = request.POST['compname'].lower()
        address = request.POST['address'].lower()
        phonenumber = request.POST['phonenumber']
        for i in visiters_details:
            if phonenumber==i.Visitors_phone_number:
                messages.error(request, 'Phone number is already exist !!!' )
                return HttpResponseRedirect("?error=1")
        hostPhonenumber = request.POST.get('HostPhoneNumber')

        purposeofvisit = request.POST['purposeofvisit'].lower()
        hostname = request.POST['hostname'].lower()
        departmentname = request.POST.get('department',False).lower()


        imageurl=request.POST['image']

        intz = pytz.timezone('Africa/Lagos')
        nowdt = datetime.now(intz)

        print("=====+++=======+++>>> host details",hostPhonenumber,hostname,departmentname)
        exist_visitor=visit.objects.filter(visitors__firstname=firstname,visitors__Visitors_phone_number=phonenumber).last()
        exist_host=Host.objects.filter(hostname=hostname,Host_phone_number=hostPhonenumber,department=departmentname)
        print("==> status of",exist_host)
        if not exist_host:
            messages.error(request, 'The host is not present in the DataBase !!!' )
            return HttpResponseRedirect("?error=1")
        if not exist_visitor:
            info=Visitors(firstname=firstname,lastname=lastname,address=address,visitor_company=compname,Visitors_phone_number=phonenumber,pourpose=purposeofvisit, blacklisted=0,imageurl=imageurl)
            info.save()
            visitor_id=Visitors.objects.get(firstname=firstname,lastname=lastname,visitor_company=compname,address=address,Visitors_phone_number=phonenumber)

            host_id=Host.objects.get(hostname=hostname,Host_phone_number=hostPhonenumber,department=departmentname)
            checkInDetails=visit(host=host_id,visitors=visitor_id,user_name=username,cheakedINinfo=1,checkInTime=nowdt,checkInDate=nowdt)
            checkInDetails.save()
            return render(request, 'visiters/checkin-conformation-details.html', {'total': count, 'CCount': CCount,'scount':Scount,'details':checkInDetails})
        else:
            if exist_visitor.cheakedINinfo==1:
                messages.error(request, 'The visitor is already checked In !! please check out first' )
                return HttpResponseRedirect("?error=1")    
            host_id=Host.objects.get(hostname=hostname,Host_phone_number=hostPhonenumber,department=department)
            visitor_id=Visitors.objects.get(firstname=exist_visitor.visitors.firstname)
            checkInDetails=visit(host=host_id,visitors=visitor_id,user_name=username,cheakedINinfo=1,checkInTime=nowdt,checkInDate=nowdt)
            checkInDetails.save()
            return render(request, 'visiters/checkin-conformation-details.html', {'total': count, 'CCount': CCount,'scount':Scount,'details':checkInDetails})
       
    return render(request, 'visiters/check-in.html',{'total': count, 'CCount': CCount,'scount':Scount,'host':host_details})

# def conformationDetails(request):
#     return render(request, 'visiters/checkin-conformation-details.html')
@login_required(login_url='/user/login/')
def checkout(request):
    count = visit.objects.filter(cheakedINinfo=1).count()
    CCount = visit.objects.filter(cheakedINinfo=2).count()
    Scount=visit.objects.filter(schedukevisit=1).count()

    host_details=Host.objects.all()
    if request.method == 'POST' and request.POST['action'] == 'gettag':
        count = visit.objects.filter(cheakedINinfo=1).count()
        CCount = visit.objects.filter(cheakedINinfo=2).count()
        Scount=visit.objects.filter(schedukevisit=1).count()
        id = request.POST['tagid']
        if (id[:3]!='RVG'):
            messages.error(request, 'ID should start with RVG !! ')
            return HttpResponseRedirect("/checkout/?error=1")
        id=id[3:]
        print("====>",id)
        if visit.objects.filter(id=id).exists():
            # tagid = Visitors.objects.get(visitorId=id)
            tagid=visit.objects.get(id=id)
            # print("=====>",tagid.visitors.firstname)
            # print("====>",tagid.checkInDate)
            # print("====>",tagid.checkInTime)
            # print("++++=====>",tagid.host.hostname)
            if tagid.schedukevisit==1:
                messages.error(request, 'No Visitor Found !!')
                return HttpResponseRedirect("/checkout/?error=1")

            if tagid.cheakedINinfo != 1:
                messages.error(request, 'No Visitor Found !!')
                return HttpResponseRedirect("/checkout/?error=1")
            else:
                return render(request, 'visiters/checkout.html', {'tagid': tagid,'total': count, 'CCount': CCount,'scount':Scount})
        else:
            messages.error(request, 'No Visitor Found !!')
            return HttpResponseRedirect("/checkout/?error=1")
            

    if request.method == "POST" and request.POST['action'] == 'checkouttag':
        count = visit.objects.filter(cheakedINinfo=1).count()
        CCount = visit.objects.filter(cheakedINinfo=2).count()
        Scount=visit.objects.filter(schedukevisit=1).count()

        id = request.POST['tagid']
        print("===>",id)
        # print("===>>",id)
        tagid=visit.objects.get(id=id)
        tagid.cheakedINinfo = 2
        intz = pytz.timezone('Africa/Lagos')
        nowdt = datetime.now(intz)
        tagid.checkOutTime=nowdt
        tagid.checkOutDate=nowdt
        tagid.save()
        return render(request, 'visiters/checkout.html', {'checkoutSuccessful': id,'total': count, 'CCount': CCount,'scount':Scount})
    return render(request, 'visiters/checkout.html',{'total': count, 'CCount': CCount,'scount':Scount,'host':host_details})

@login_required(login_url='/user/login/')
def takeimg(request):
    return render(request, 'visiters/dashbord.html',{'username':username})

@login_required(login_url='/user/login/')
def users(request):
    return render(request, 'visiters/users.html')


@login_required(login_url='/user/login/')
def visiterslist(request):
    return render(request, 'visiters/visiterslist.html')

@login_required(login_url='/user/login/')
def report(request):
    return render(request, 'visiters/reports.html')

@login_required(login_url='/user/login/')
def schedulevisit(request):
    count = visit.objects.filter(cheakedINinfo=1).count()
    CCount = visit.objects.filter(cheakedINinfo=2).count()
    Scount=visit.objects.filter(schedukevisit=1).count()
    host_details=Host.objects.all()
    visiters_details=Visitors.objects.all()
    print("in the schedule visit")
    username=request.user.username
    print(username)

    if request.method=='POST' and request.POST['action']=='visit':
        count = visit.objects.filter(cheakedINinfo=1).count()
        CCount = visit.objects.filter(cheakedINinfo=2).count()
        Scount=visit.objects.filter(schedukevisit=1).count()
        id=request.POST['tagid']
        if (id[:3]!='RVG'):
            messages.error(request, 'ID should start with RVG !! ')
            return HttpResponseRedirect("/?error=1")
        id=id[3:]

        if visit.objects.filter(visitors__visitorId=id).exists():
            tagid=visit.objects.get(visitors__visitorId=id)
            print("====fasjdfalskjfn as====== ",tagid)
            if tagid.schedukevisit==1:
                return render(request, 'visiters/schedule.html',{'tagid':tagid,'total': count, 'CCount': CCount,'scount':Scount})
        else:
            messages.error(request, 'User Not found!! ')
            return HttpResponseRedirect("/schedulevisit/?error=1")
    if request.method=='POST' and request.POST['action']=='schedulevisit':
        count = visit.objects.filter(cheakedINinfo=1).count()
        CCount = visit.objects.filter(cheakedINinfo=2).count()
        Scount=visit.objects.filter(schedukevisit=1).count()
        allschedulevisits=visit.objects.filter(schedukevisit=1)
        return render(request, 'visiters/schedule.html',{'total': count, 'CCount': CCount,'scount':Scount,'schedulevisits':allschedulevisits})

    if request.method=='POST' and request.POST['action']=='sc':
        count = visit.objects.filter(cheakedINinfo=1).count()
        CCount = visit.objects.filter(cheakedINinfo=2).count()
        Scount=visit.objects.filter(schedukevisit=1).count()
        firstname=request.POST['firstname'].lower()
        lastname=request.POST['lastname'].lower()
        hostPhonenumber = request.POST.get('HostPhoneNumber')
        phonenumber=request.POST['Visiterphonenumber']


        CompanyName=request.POST['compname']
        address=request.POST['address']
        purposeVisit=request.POST['purposeofvisit']

        for i in visiters_details:
            if phonenumber==i.Visitors_phone_number:
                messages.error(request, 'Phone number is already exist !!!' )
                return HttpResponseRedirect("/schedulevisit/?error=1")
        hostname=request.POST['hostname'].lower()
        department=request.POST.get('department').lower()
        date=request.POST['date']
        time=request.POST['time']
        pin=randint(1000, 9999)

        exist_visitor=visit.objects.filter(visitors__firstname=firstname,visitors__lastname=lastname,visitors__Visitors_phone_number=phonenumber).last()
        print("the visit details is ==+>",exist_visitor)
        exist_host=Host.objects.filter(hostname=hostname,Host_phone_number=hostPhonenumber,department=department)
        if not exist_host:
            messages.error(request, 'The host is not present in the DataBase !!!' )
            return HttpResponseRedirect("/schedulevisit/?error=1")
        if not exist_visitor:
            try:

                info=Visitors(firstname=firstname,lastname=lastname,Visitors_phone_number=phonenumber,address=address,visitor_company=CompanyName,pourpose=purposeVisit, blacklisted=0)

                info.save()
                visitor_id=Visitors.objects.get(firstname=firstname,lastname=lastname,Visitors_phone_number=phonenumber)
                host_id=Host.objects.get(hostname=hostname,Host_phone_number=hostPhonenumber,department=department)
                checkInDetails=visit(host=host_id,visitors=visitor_id,user_name=username,cheakedINinfo=0,schedukevisit=1,schedule_date=date,schedule_time=time,schedule_pin=pin)
                checkInDetails.save()
            except IntegrityError as e: 
                visitor_id.delete()
                schedulevisit(request)
            return render(request, 'visiters/checkin-conformation.html', {'total': count, 'CCount': CCount,'scount':Scount,'pin':pin,'date':date,'time':time})
        else:
            print("visitor exist")
            if exist_visitor.cheakedINinfo==1:
                messages.error(request, 'The visitor is already checked In !! Please check out first ' )
                return HttpResponseRedirect("/schedulevisit/?error=1")
            try:
                host_id=Host.objects.get(hostname=hostname,Host_phone_number=hostPhonenumber,department=department)
                visitor_id=Visitors.objects.get(firstname=exist_visitor.visitors.firstname)
                checkInDetails=visit(host=host_id,visitors=visitor_id,user_name=username,cheakedINinfo=0,schedule_pin=pin,schedule_date=date,schedule_time=time)
                checkInDetails.save()
            except IntegrityError as e: 
                visitor_id.delete()
                schedulevisit(request)
            return render(request, 'visiters/checkin-conformation.html', {'total': count, 'CCount': CCount,'scount':Scount,'pin':pin,'date':date,'time':time})
        messages.error(request, 'some thing wents wrong !!!' )
        return HttpResponseRedirect("/?error=1")
    if request.method=='POST' and request.POST['action']=='delete':
        count = visit.objects.filter(cheakedINinfo=1).count()
        CCount = visit.objects.filter(cheakedINinfo=2).count()
        Scount=visit.objects.filter(schedukevisit=1).count()
        tegid=request.POST['tagid']
        t=visit.objects.get(id=tegid)
        t.delete()
        return redirect('/schedulevisit/')
    return render(request, 'visiters/schedule.html',{"sucess":1,'total': count, 'CCount': CCount,'scount':Scount ,'host':host_details})


@login_required(login_url='/user/login/')
def deleteschedulevisit(request,id):
    return render(request, 'visiters/schedule.html')


@login_required(login_url='/user/login/')
def seating(request):
    count = visit.objects.filter(cheakedINinfo=1).count()
    CCount = visit.objects.filter(cheakedINinfo=2).count()
    Scount=visit.objects.filter(schedukevisit=1).count()
    form = setting.objects.get(id=1)
    return render(request, 'visiters/seating.html',{'form': form, 'total': count, 'CCount': CCount,'scount':Scount})


def goimage(request):
    return render(request,'visiters/goimage.html')

# ------------------------------------------------------------------------------------------
# Show Visitor List
def show_visitors(request):
    visit_obj = visitobj()
    v_obj = visit.objects.all().exclude(checkInTime = None)
    return render(request, 'visiters/visiterslist.html', {'form': v_obj, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})


def search_visitors(request):
    visit_obj = visitobj()
    name_val = request.POST.get('search').lower().strip()
    val = [x.strip() for x in name_val.split()]
    if len(val) == 1:
        form = visit.objects.filter(visitors__firstname=val[0])
    else:
        form = visit.objects.filter(visitors__firstname=val[0], visitors__lastname=val[1])
    if not form:
        messages.error(request, 'No User Found')
        return redirect('/show_visiter/')
    else:
        print(val)
        return render(request, 'visiters/search_visiterslist.html', {'form': form, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})


# User to Blank
def user_to_blank(request, id):
    visit_obj = visitobj()
    if request.user.profile.role == 'admin':
        val = Visitors.objects.get(visitorId=id)
        val.blacklisted = 0
        val.save()
        return render(request, 'visiters/notify_user_converted.html', {'form': 'Unlisted', 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
    else:
        return HttpResponseRedirect('/show_visiter/')


# User to blacklist
def user_to_blacklist(request, id):
    visit_obj = visitobj()
    if request.user.profile.role == 'admin':
        val = Visitors.objects.get(visitorId=id)
        val.blacklisted = 2
        val.save()
        return render(request, 'visiters/notify_user_converted.html', {'form': 'Blacklisted', 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
    else:
        return HttpResponseRedirect('/show_visiter/')


# User to whitelist
def user_to_whitelist(request, id):
    visit_obj = visitobj()
    if request.user.profile.role == 'admin':
        val = Visitors.objects.get(visitorId=id)
        val.blacklisted = 1
        val.save()
        return render(request, 'visiters/notify_user_converted.html', {'form': 'Whitelisted', 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
    else:
        return HttpResponseRedirect('/show_visiter/')


#  Show WhiteList Visitors
def visitor_whitelist(request):
    visit_obj = visitobj()
    if 'search' in request.GET:
        name_val = request.GET.get('search').lower().strip()
        val = [x.strip() for x in name_val.split()]
        if len(val) == 1:
            form = visit.objects.filter(visitors__firstname=val[0], visitors__blacklisted=1)
        else:
            form = visit.objects.filter(visitors__firstname=val[0], visitors__lastname=val[1], visitors__blacklisted=1)

        if not form:
            messages.error(request, 'No User Found')
            return render(request, 'visiters/visiters_whitelist.html', {'form': form, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
        else:
            return render(request, 'visiters/visiters_whitelist.html', {'form': form, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
    else:
        form = visit.objects.filter(visitors__blacklisted=1)
        return render(request, 'visiters/visiters_whitelist.html', {'form': form, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})


# Show BlackList Visitors
def visitor_blacklist(request):
    visit_obj = visitobj()
    if 'search' in request.GET:
        name_val = request.GET.get('search').lower().strip()
        val = [x.strip() for x in name_val.split()]
        if len(val) == 1:
            form = visit.objects.filter(visitors__firstname=val[0], visitors__blacklisted=2)
        else:
            form = visit.objects.filter(visitors__firstname=val[0], visitors__lastname=val[1], visitors__blacklisted=2)
        if not form:
            messages.error(request, 'No User Found')
            return render(request, 'visiters/visiters_blacklist.html', {'form': form, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
        else:
            return render(request, 'visiters/visiters_blacklist.html', {'form': form, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
    else:
        form = visit.objects.filter(visitors__blacklisted=2)
        return render(request, 'visiters/visiters_blacklist.html', {'form': form, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})

# Show Reports
def user_reports(request):
    visit_obj = visitobj()
    if request.method == 'GET':
        if 'Visitors' in request.GET:
            name_val = request.GET.get('visitor_name').lower().strip()
            v_name = [x.strip() for x in name_val.split()]
            vperiod_to = request.GET.get('vperiod_to')
            vperiod_from = request.GET.get('vperiod_from')
            if not v_name:
                v_name = False
            if not vperiod_from:
                vperiod_from = False

            if v_name and len(v_name) == 2 and vperiod_from and vperiod_to:
                form = visit.objects.filter(visitors__firstname=v_name[0], visitors__lastname=v_name[1],
                                            checkInDate__gte=vperiod_from,checkInDate__lte=vperiod_to)
            elif not v_name and vperiod_from and vperiod_to:
                form = visit.objects.filter(checkInDate__gte=vperiod_from, checkInDate__lte=vperiod_to)
            elif v_name and len(v_name) == 2 and vperiod_from:
                form = visit.objects.filter(visitors__firstname=v_name[0], visitors__lastname=v_name[1],
                                            checkInDate=vperiod_from)
            elif not v_name and vperiod_from:
                form = visit.objects.filter(checkInDate=vperiod_from)
            elif v_name and len(v_name) == 2:
                form = visit.objects.filter(visitors__firstname=v_name[0], visitors__lastname=v_name[1])
            elif v_name and len(v_name) == 1:
                form = visit.objects.filter(visitors__firstname=v_name[0])
            else:
                form = None
            if not form:
                messages.error(request, "No Details Found")
                return render(request, 'visiters/reports.html', {'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
            else:
                li = []
                for i in form:
                    li.append(i.id)
                return render(request, 'visiters/reports.html', {'form': form, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2], 'form_values':li})
    return render(request, 'visiters/reports.html', {'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})


def print_userReport(request, value):
    str =''
    for i in range(1, len(value) - 1):
        str = str + value[i]
    val = [int(x) for x in str.split(",")] 
    li = []
    for id in val:
        val = visit.objects.get(pk=id)
        li.append(val)
    comp_name = setting.objects.get(id=1)
    company_obj = comp_name.compName
    return render(request, 'visiters/printUser_report.html', {'form':li, 'company':company_obj})


def print_hostReport(request, value):
    str =''
    for i in range(1, len(value) - 1):
        str = str + value[i]
    val = [int(x) for x in str.split(",")] 
    li = []
    for id in val:
        val = visit.objects.get(pk=id)
        li.append(val)
    comp_name = setting.objects.get(id=1)
    company_obj = comp_name.compName
    return render(request, 'visiters/printUser_report.html', {'form':li, 'company':company_obj})



def report_host(request):
    visit_obj = visitobj()
    if 'Hosts' in request.GET:
            h_name = request.GET.get('host_name').lower().strip()
            hp_from = request.GET.get('hperiod_from')
            hp_to = request.GET.get('hperiod_to')
            if not h_name:
                h_name = False
            if not hp_from:
                hp_from = False
            if h_name and hp_from and hp_to:
                form = visit.objects.filter(host__hostname__contains=h_name, checkInDate__gte=hp_from, checkInDate__lte=hp_to)
            elif hp_from and hp_to:
                form = visit.objects.filter(checkInDate__gte=hp_from, checkInDate__lte=hp_to)
            elif h_name and hp_from:
                form = visit.objects.filter(host__hostname__contains=h_name, checkInDate=hp_from)
            elif hp_from:
                form = visit.objects.filter(checkInDate=hp_from)
            else:
                form = visit.objects.filter(host__hostname__contains=h_name)
            if not form:
                messages.error(request, "No Details Found")
                return render(request, 'visiters/reports_hosts.html', {'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
            else:
                li = []
                for i in form:
                    li.append(i.id)
                return render(request, 'visiters/reports_hosts.html', {'form1': form, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2], 'form_values':li})
    return render(request, 'visiters/reports_hosts.html', {'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})


def weekly_report(request):
    visit_obj = visitobj()
    current_date = datetime.now().date()
    week = datetime.now().date() - timedelta(days=7)
    form = visit.objects.filter(checkInDate__gte=week)
    return render(request, 'visiters/weekly_report.html', {'form': form, 'total': visit_obj[0], 'CCount': visit_obj[1],
                                                           'scount': visit_obj[2], 'beforedate': week, 'currentdate': current_date})


def print_weeklyreport(request):
    week = datetime.now().date() - timedelta(days=7)
    form = visit.objects.filter(checkInDate__gte=week)
    comp_name = setting.objects.get(id=1)
    company_obj = comp_name.compName
    return render(request, 'visiters/print_weekly_report.html', {'form':form, 'company':company_obj})

def print_monthlyreport(request):
    month = datetime.now().month
    form = visit.objects.filter(checkInDate__month=month)
    comp_name = setting.objects.get(id=1)
    company_obj = comp_name.compName
    return render(request, 'visiters/print_weekly_report.html', {'form':form, 'company':company_obj})


def monthly_report(request):
    visit_obj = visitobj()
    month = datetime.now().month
    datetime_object = datetime.strptime(str(month), "%m")
    full_month_name = datetime_object.strftime("%B")
    form = visit.objects.filter(checkInDate__month=month)
    return render(request, 'visiters/monthly_report.html', {'form': form, 'total': visit_obj[0], 'CCount': visit_obj[1],
                                                            'scount': visit_obj[2], 'month':full_month_name})


def edit_settings(request):
    visit_obj = visitobj()
    if request.user.profile.role == 'admin':
        if request.method == 'POST':
            
            name_obj = request.POST['company_name']
            email_obj = request.POST['company_email']
            val = setting.objects.get(id=1)
            if len(request.FILES) != 0:
                image_obj = request.FILES['image_field']
                val.compLogo = image_obj
            val.compName = name_obj
            val.compEmail = email_obj
            val.save()
            return HttpResponseRedirect('/setting/')
        else:
            form = setting.objects.get(id=1)
            return render(request, 'visiters/setting_edit.html', {'total': visit_obj[0], 'CCount': visit_obj[1],
                                                            'scount': visit_obj[2], 'form': form})
    else:
        return HttpResponseRedirect('/setting/')


def visitobj():
    count = visit.objects.filter(cheakedINinfo=1).count()
    CCount = visit.objects.filter(cheakedINinfo=2).count()
    Scount = visit.objects.filter(schedukevisit=1).count()
    return count, CCount, Scount


def printtag_list(request):
    visit_obj = visitobj()
    if 'search' in request.GET:
        val = request.GET.get('search').lower().strip()
        v_name = [x.strip() for x in val.split()]
        if len(v_name) == 1:
            form = print_tag.objects.filter(first_name=v_name[0])
        elif len(v_name) == 2:
            form = print_tag.objects.filter(first_name=v_name[0], last_name=v_name[1])
        else:
            form = None
        if not form:
            messages.error(request, 'No User Found')
            form1 = print_tag.objects.all()
            return render(request, 'visiters/tag_details.html', {'form': form1, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
        else:
            return render(request, 'visiters/tag_details.html', {'form': form, 'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})
    else:
        print_obj = print_tag.objects.all().order_by("-checkout_Date")
        print(print_obj)
        tag_count = print_tag.objects.filter(status=1).count()
        return render(request, 'visiters/tag_details.html', {'form': print_obj, 'printtag_count':tag_count ,'total': visit_obj[0], 'CCount': visit_obj[1], 'scount': visit_obj[2]})


def cardPrint_byPhone(request,id):
    checkInDetails=print_tag.objects.get(id=id)
    checkInDetails.status = 0
    checkInDetails.save()
    return render(request, 'visiters/printTag_byPhone.html',{'print_details':checkInDetails})


def cardPrint_delete(request,id):
    tag=print_tag.objects.get(id=id)
    tag.delete()
    return HttpResponseRedirect('/printtag_details/')


def cardPrint(request,id):
    checkInDetails=visit.objects.get(id=id)
    return render(request, 'visiters/details.html',{'details':checkInDetails})

@login_required(login_url='/user/login/')
def upload_host(request):
    if request.method == 'POST':
        if len(request.FILES) == 1:
            file = request.FILES['host_list']
            if not file.name.endswith('.csv'):
                messages.error(request, 'Please make sure that you are uploading CSV file only')
            else:
                try:
                    file_data = file.read().decode('utf-8')
                    rows = file_data.splitlines(True)
                    row_id = 0
                    for row in rows:
                        if row_id != 0:
                            columns = row.split(',')
                            host = Host(hostname=columns[0], Host_phone_number=columns[1], department=columns[2])
                            host.save()
                        else:
                            row_id += 1
                    messages.success(request, 'Host\'s details are saved successfully.')
                except:
                    messages.error(request, 'Please make sure that uploaded file have data in correct format.')
        else:
            messages.error(request, 'Please upload the csv file with host\'s details.')
        return render(request, 'visiters/upload.html')
    else:
        return render(request, 'visiters/upload.html')
