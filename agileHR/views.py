import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Training, Employee, EmployeeTraining

def index(request):
    context = {}
    return render(request, 'agileHR/index.html', context)

def employee(request):
    context = {}
    return render(request, 'agileHR/employee.html', context)

def department(request):
    context = {}
    return render(request, 'agileHR/department.html', context)

def training(request):
    training_list = Training.objects.filter(start_date__date__gte=datetime.date.today()).order_by('start_date')
    context = {'training_list': training_list}
    return render(request, "agileHR/training.html", context)

def computer(request):
    context = {}
    return render(request, 'agileHR/computer.html', context)

def traindetail(request, training_id):
    training = get_object_or_404(Training, pk=training_id)
    context = {'training': training}
    return render(request, 'agileHR/training_detail.html', context)
