from django.urls import path
from . import views
urlpatterns = [
    path("sponser-create/", views.SponserCreateAPIView.as_view()),
    path("sponser-list/", views.SponserListAPIView.as_view()),
    path("sponser-detail/<int:pk>", views.SponserDetailAPIView.as_view()),
    path("sponser-update/<int:pk>", views.SponserUpdateAPIView.as_view()),
# ----------------------------------------------------------------------------------
    path("studentsponser-create/", views.StudentSponserCreateAPIView.as_view()),
# ----------------------------------------------------------------------------------
    path("student-create/", views.StudentCreateAPIView.as_view()),
    path("student-list/", views.StudentListAPIView.as_view()),
    path("student-update/", views.StudentUpdateAPIView.as_view()),
# ----------------------------------------------------------------------------------
    path("dashboard-statistic/", views.DashboardStatisticAPIView.as_view()),
    path("dashboard-graphic/", views.GraphicAPIView.as_view())
# ----------------------------------------------------------------------------------
]