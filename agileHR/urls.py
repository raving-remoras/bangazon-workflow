from django.urls import path
from . import views

app_name = "agileHR"
urlpatterns = [
    path("", views.index, name="index"),
    path("employees/", views.employee, name="employee"),
    path("employees/<int:employee_id>/", views.employee_detail, name="employee_detail"),
    path("departments/", views.department, name="department"),
    # ex: /agileHR/trainings/
    path("trainings/", views.training, name="training"),
    # ex: /agileHR/trainings/5
    path("trainings/<int:training_id>", views.traindetail, name="traindetail"),
    # ex: /agileHR/computers/
    path("computers/", views.computer, name="computer"),
    # ex: /agileHR/computers/12
    path("computers/<int:computer_id>", views.computer_detail, name="computer_detail")
]

