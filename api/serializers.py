from rest_framework import serializers
from . import models
from django.db.models import Sum
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
# ---------------------------------------------------------------------------------------

class SponserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sponser
        fields = (
            'full_name',
            'phone_number',
            'organization_name',
            'amount',
            'type'
        )

        extra_kwargs = {
            "id" : {
                "read_only": True
            }
        }


    def validate(self, attr):
        print(attr)
        type = attr.get('type')
        organization_name = attr.get('organization_name')
        # type == 'PHYSICAL'
        # organization_name != None
        if type == 'physical' and organization_name:
            raise serializers.ValidationError(detail={"error": "Jismoniy shaxs tashkilot nomiga ega emas"})        



        # if type == 'legal' and not organization_name:
        #     raise serializers.ValidationError(detail={"error": "Yuridik shaxs tashkilot nomiga ega bo'lishi shart!"})        

        return attr

    def create(self, validated_data):
        organization_name = models.Sponser.objects.create(**validated_data)
        return organization_name
    
# --------------------------------------------------------------------------------------------

class SponserListSerializer(serializers.ModelSerializer):
    
    sponser_amount = serializers.SerializerMethodField()
    def get_sponser_amount(self, obj):
        a = obj.student_sponsers.aggregate(Sum('amount'))
        return a['amount__sum'] if a['amount__sum'] else 0
    
    class Meta:
        model = models.Sponser
        fields = (
            'id',
            'full_name',
            'phone_number',
            'amount',
            'created_at',
            'status',
            'sponser_amount'
        )

# -------------------------------------------------------------------------------

class SponserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sponser
        fields = "__all__"

# --------------------------------------------------------------------------------

class SponserStudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StudentSponser
        fields = "__all__"
    
    def create(self, validated_data):
        amount = validated_data.get('amount')
        student = validated_data.get("student")
        sponser = validated_data.get("sponser")

    # soralgan summa oshib ketmasligi kerak

        total_amount = sum(models.StudentSponser.objects.filter(student=student).values_list("amount", flat=True))


        if total_amount + amount > student.contract:
            raise serializers.ValidationError(detail=(f"{student.contract - total_amount - amount}dan kop bolmasligi kerak"))

        sponser_amount = sum(models.StudentSponser.objects.filter(sponser=sponser).values_list("amount", flat=True))


        if sponser_amount > sponser.amount:
            raise serializers.ValidationError(detail=(f"{sponser.amount} ...."))
        
        return super().create(validated_data)

#  ----------------------------------------------------------------------------------

class StudentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = (
            "full_name",
            "university",
            "contract",
            "degree"
        )

        extra_kwargs = {
            "id": {
                "read_only": True
            }
        }

# ---------------------------------------------------------------------------------------

class StudentListSerializer(serializers.ModelSerializer):

    student_amount = serializers.SerializerMethodField() # SerializerMethodField - qo'lda yoziladigan polya uchun kerak bo'ladi
    def get_student_amount(self, obj):
        result = sum(models.StudentSponser.objects.filter(student=obj).values_list("amount", flat=True))
        print(result)
        return result
        
    class Meta:
        model = models.Student
        fields = (
            "id",
            "full_name",
            "degree",
            "university",
            "student_amount",
            "contract",
            "student_amount"
        )

# -----------------------------------------------------------------------------------

class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = "__all__"

# ------------------------------------------------------------------------------------
