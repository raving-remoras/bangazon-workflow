from django.urls import path
from . import views

app_name = "agileHR"
urlpatterns = [
    path("", views.index, name="index"),
    path("employees/", views.employee, name="employee"),
    path("employees/<int:employee_id>/", views.employee_detail, name="employee_detail"),
    path("departments/", views.department, name="department"),
    path("departments/<int:dept_id>/", views.department_detail, name="department_detail"),
    path("trainings/", views.training, name="training"),
    path("computers/", views.computer, name="computer")
]