from django.contrib import admin
from .models import * 


@admin.register(Sponser)
class SponserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "organization_name", "amount", "status")
    list_display_links = ("full_name",) 
    search_fields = ("full_name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "university", "contract", "degree")
    list_display_links = ("full_name",)
    search_fields = ("full_name",)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)
    search_fields = ("name",)


@admin.register(StudentSponser)
class StudentSponserAdmin(admin.ModelAdmin):
    list_display = ("sponser", "student", "amount")
    list_display_links = ("sponser", "student", "amount")
    search_fields = ("sponser", "student")
