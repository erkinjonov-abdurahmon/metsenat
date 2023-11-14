from django.shortcuts import render
from . import serializers, models, paginations
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView, Response
from django.db.models import Sum
from datetime import date, timedelta
import calendar

class SponserCreateAPIView(CreateAPIView):
    queryset = models.Sponser.objects.all()
    serializer_class = serializers.SponserCreateSerializer

class SponserListAPIView(ListAPIView):
    queryset = models.Sponser.objects.all()
    serializer_class = serializers.SponserListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ("full_name",)
    filterset_fields = ("created_at", "status", "amount")
    pagination_class = paginations.MyOffsetPagination



class SponserDetailAPIView(RetrieveAPIView):
    queryset = models.Sponser.objects.all()
    serializer_class = serializers.SponserCreateSerializer


class SponserUpdateAPIView(UpdateAPIView):
    queryset = models.Sponser.objects.all()
    serializer_class = serializers.SponserUpdateSerializer



class StudentSponserCreateAPIView(CreateAPIView):
    queryset = models.StudentSponser.objects.all()
    serializer_class = serializers.SponserStudentCreateSerializer


class StudentCreateAPIView(CreateAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentCreateSerializer


class StudentListAPIView(ListAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentListSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_filter = ("full_name",)
    filterset_fields = ("degree", "university")
    pagination_class = paginations.OffsetPagination


class StudentUpdateAPIView(UpdateAPIView):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentUpdateSerializer


#    
#    Dashboard


class DashboardStatisticAPIView(APIView):

    def get(self, request):
        total_aid_money = models.StudentSponser.objects.aggregate(Sum("amount"))['amount__sum']
        total_contract = models.Student.objects.aggregate(Sum("contract"))['contract__sum']
        return Response({
            "total_paid_money": total_aid_money,
            "total_contract": total_contract,
            "total_left_money": total_contract - total_aid_money
        })


class GraphicAPIView(APIView):

    def get(self, request):

        this_year = date.today().year
        start_date = date(this_year, 1, 1)
        end_date = date(this_year, 12, 31)
        result = []

        while start_date < end_date:
            this_year = start_date.year
            this_month = start_date.month
            num_days = calendar.monthrange(this_year, this_month)[1]
            queryset = models.Sponser.objects.filter(created_at__range=(start_date, date(this_year, this_month, num_days))).count()
            result.append({
                "month": start_date.strftime("%B"),
                "sposer_count": queryset,

            })
            start_date += timedelta(days=num_days)

        return Response(result)
    
    