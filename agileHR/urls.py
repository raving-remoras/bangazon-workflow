from django.urls import path
from . import views

app_name = "agileHR"
urlpatterns = [
    path("", views.index, name="index"),
    path("employees/", views.employee, name="employee"),
    path("departments/", views.department, name="department"),
    # ex: /agileHR/trainings/
    path("trainings/", views.training, name="training"),
    # ex: /agileHR/trainings/5
    path("trainings/<int:training_id>", views.traindetail, name="traindetail"),
    path("computers/", views.computer, name="computer"),
]

