from rest_framework import serializers
from .models import Visitors, Company, Host, visit


class visitors_serializer(serializers.ModelSerializer):
    class Meta:
        model = Visitors
        fields = ('visitorId', 'firstname', 'lastname', 'address', 'Visitors_phone_number',
                  'pourpose', 'blacklisted',
                  'imageurl', 'visitor_company')


class company_serializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('companyName', 'companyLogo', 'companyEmail')


class host_serializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ('hostname', 'Host_phone_number', 'department')


class visit_serializer(serializers.ModelSerializer):
    class Meta:
        model = visit
        fields = ('visitors', 'host', 'checkInDate', 'checkOutDate',
                  'checkInTime', 'checkOutTime', 'cheakedINinfo', 'schedukevisit')

    def create(self, validated_data):
        return visit.objects.create(**validated_data)
