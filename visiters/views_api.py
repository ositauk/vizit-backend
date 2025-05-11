from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Visitors, visit, Host, Company, print_tag
from .serializers import *
from rest_framework import status

from datetime import datetime, timedelta
import pytz


# get user data
class search_visitor(APIView):
    def get(self, request, pk):
        pin = pk
        try:
            stu = visit.objects.get(schedule_pin=pin)
            if stu.schedukevisit == 0:
                response = {'message': "Pin Invalid"}
                return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except:
            stu = None
        if not stu:
            response = {'message': "Pin Invalid"}
            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        visit_id = stu.id
        visitorid_obj = stu.visitors.visitorId
        host_name = stu.host.hostname
        visitor_data = Visitors.objects.get(visitorId=visitorid_obj)
        serializer = visitors_serializer(visitor_data)
        response = {'visit_id': visit_id, 'data': serializer.data, 'host_name': host_name}
        return Response(response)

    # User checked in after we searched by pin
    def put(self, request, pk):
        try:
            visit_obj = visit.objects.get(id=pk)
        except:
            visit_obj = None
        if not visit_obj:
            response = {'message': "User Invalid"}
            return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        response = {'message': 'User Checked In'}
        return Response(response)


# Get all host details
class host_details(APIView):
    def get(self, request):
        host_obj = Host.objects.all()
        host_serializer_obj = host_serializer(host_obj, many=True)
        return Response(host_serializer_obj.data)


# Post/create user
class visitapi(APIView):
    def post(self, request):
        response = {'message': "Something went's wrong"}

        print("in visit")

        try:
            f_name = request.data['first_name'].lower()
            l_name = request.data['last_name'].lower()
            company_name = request.data['company_name']
            contact = request.data['contact_address']
            number = request.data['phone_number']
            purpose = request.data['purpose']
            hostname = request.data['host_name']

            Host_phonenumber = request.data['Host_phone_number']
            department = request.data['department']
            exist_visitor = visit.objects.filter(visitors__firstname=f_name, visitors__lastname=l_name, visitors__Visitors_phone_number=number)
            exist_host = Host.objects.filter(hostname=hostname, Host_phone_number=Host_phonenumber, department=department)
            print('=========>', exist_visitor, exist_host)

            if not exist_host:
                response2 = {'message': "Host not present"}
                return Response(response2, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            if not exist_visitor:

                print("not exist visitor")
                info = Visitors(firstname=f_name, blacklisted=0, lastname=l_name, pourpose=purpose,
                                address=contact, Visitors_phone_number=number, visitor_company=company_name)
                info.save()
                print( "80")
                visitor_id = Visitors.objects.get(firstname=f_name, lastname=l_name, Visitors_phone_number=number)
                visitor_obj = visitor_id.visitorId
                host_id = Host.objects.get(hostname=hostname, Host_phone_number=Host_phonenumber, department=department)
                checkInDetails = visit(host=host_id, visitors=visitor_id)
                checkInDetails.save()
                visit_obj = visit.objects.filter(host=host_id, visitors=visitor_id).last()
                visit_id = visit_obj.id
                response = {'message': "Updated",'visit_id': visit_id, 'visitor_id': visitor_obj}
                return Response(response)
            else:
                print("else part exist visitor")
                if exist_visitor[0].cheakedINinfo == 1:
                    response2 = {'message': "The visitor is already checked In...!!"}
                    return Response(response2, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                
                if exist_visitor[0].visitors.blacklisted == 2:
                    response2 = {'message': "The visitor is Blacklisted...!!"}
                    return Response(response2, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                else:    
                    host_id = Host.objects.get(hostname=hostname, Host_phone_number=Host_phonenumber, department=department)
                    visitor_id = Visitors.objects.get(firstname=f_name, lastname=l_name, Visitors_phone_number=number)
                    visitor_obj = visitor_id.visitorId
                    checkIn = visit(host=host_id, visitors=visitor_id)
                    checkIn.save()
                    visit_obj = visit.objects.filter(host=host_id, visitors=visitor_id).last()
                    visit_id = visit_obj.id
                    response = {'message': "Updated",'visit_id': visit_id, 'visitor_id': visitor_obj}
                    return Response(response)

        except Exception as e:
            print(e)
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class image_upload(APIView):
    def put(self, request, pk):
        response = {'message': 'Please Try again visitor not available'}
        try:
            image_obj = request.data['image']
            user_obj = Visitors.objects.get(visitorId=pk)
            user_obj.imageurl = image_obj
            user_obj.save()

            response = {'message': 'Image Uploaded'}
            return Response(response)
        except Exception as e:
            print(e)
        return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



# print id tag
class printtag_details(APIView):
    def get(self, request, pk):
        response = {'message': 'Please Try again visitor not available'}
        try:

            intz = pytz.timezone('Africa/Lagos')
            nowdt = datetime.now(intz)
            user_obj = visit.objects.get(pk=pk)
            user_obj.cheakedINinfo = 1
            user_obj.schedukevisit = 0
            user_obj.checkInTime = nowdt
            user_obj.checkInDate = nowdt

            user_obj.save()
            f_name = user_obj.visitors.firstname
            l_name = user_obj.visitors.lastname
            host = user_obj.host.hostname
            checkintime = user_obj.checkInTime
            checkindate = user_obj.checkInDate
            image_url = user_obj.visitors.imageurl
            printdetail = print_tag(visit_id=user_obj, first_name=f_name, last_name=l_name, checkin_Time=checkintime, 
            checkout_Date=checkindate, host_name=host, status=1, imageurl=image_url)
            printdetail.save()
            response = {'message': 'Sent Print Request'}
            return Response(response)
        except Exception as e:
            print(e)
        return Response(response, status=status.HTTP_422_UNPROCESSABLE_ENTITY)