from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Employee, Department, Training, Computer

def index(request):
    context = {}
    return render(request, "agileHR/index.html", context)

def employee(request):
    employee_list = Employee.objects.all()
    context = {'employee_list': employee_list}
    return render(request, 'agileHR/employee.html', context)

def department(request):
    departments = Department.objects.all()
    employees = Employee.objects.all()
    context = {
        "departments": departments,
        "employees": employees
    }
    return render(request, "agileHR/department.html", context)

def training(request):
    context = {}
    return render(request, "agileHR/training.html", context)

def computer(request):
    context = {}
    return render(request, "agileHR/computer.html", context)