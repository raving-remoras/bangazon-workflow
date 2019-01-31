from django.urls import path
from . import views

app_name = "agileHR"
urlpatterns = [
    path("", views.index, name="index"),
    path("employees/", views.employee, name="employee"),
    path("employees/<int:employee_id>/", views.employee_detail, name="employee_detail"),
    path("employees/add", views.employee_add, name="employee_add"),
    path("departments/", views.department, name="department"),
    path('departments/add', views.departmentadd, name='departmentadd'),
    path("departments/<int:dept_id>/", views.department_detail, name="department_detail"),
    # ex: /bangazon/trainings/
    path("trainings/", views.training, name="training"),
    # ex: /bangazon/trainings/previous
    path("trainings/previous", views.training_past, name="training_past"),
    # ex: /bangazon/trainings/5
    path("trainings/<int:training_id>", views.training_detail, name="traindetail"),
    # ex: /bangazon/trainings/5/edit
    path("trainings/<int:training_id>/edit", views.training_edit, name="training_edit"),
    # ex: /bangazon/trainings/5/delete
    path("trainings/<int:training_id>/delete", views.training_delete, name="training_delete"),
    # ex: /bangazon/trainings/add
    path("trainings/add", views.training_add, name="training_add"),
    # ex: /bangazon/computers/
    path("computers/", views.computers, name="computers"),
    # ex: /bangazon/computers/12
    path("computers/<int:computer_id>/", views.computer_detail, name="computer_detail"),
    path("computers/<int:computer_id>/delete", views.delete_computer, name="delete_computer"),
    # ex: /bangazon/computers/new
    path("computers/new/", views.new_computer, name="new_computer")

]