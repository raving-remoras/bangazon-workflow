from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Department

def index(request):
    context = {}
    return render(request, "agileHR/index.html", context)

def employee(request):
    context = {}
    return render(request, "agileHR/employee.html", context)

def department(request):
    departments = get_object_or_404(Department)
    context = {
        "departments": departments
    }
    return render(request, "agileHR/department.html", context)

def training(request):
    context = {}
    return render(request, "agileHR/training.html", context)

def computer(request):
    context = {}
    return render(request, "agileHR/computer.html", context)