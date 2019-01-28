from django.urls import path
from . import views

app_name = "agileHR"
urlpatterns = [
    path("", views.index, name="index"),
    path("employees/", views.employee, name="employee"),
    path("departments/", views.department, name="department"),
    path("trainings/", views.training, name="training"),
    path("computers/", views.computer, name="computer")
]