from django.shortcuts import render
from django.http import HttpResponse

from .models import *

def index(request):
    context = {}
    return render(request, 'agileHR/index.html', context)

def employee(request):
    employee_list = Employee.objects.all()
    context = {'employee_list': employee_list}
    return render(request, 'agileHR/employee.html', context)

def department(request):
    context = {}
    return render(request, 'agileHR/department.html', context)

def training(request):
    context = {}
    return render(request, 'agileHR/training.html', context)


def computer(request):
    """Displays the list of computers currently owned by the company with links to details for each one.

    Author: Sebastian Civarolo

    Returns:
        render -- loads the computer.html template.
    """

    computers = Computer.objects.all()
    context = {
        "computers": computers
    }
    return render(request, 'agileHR/computer.html', context)


def computer_detail(request, computer_id):
    """Displays the details about a single computer owned by the company.

    Arguments:
        computer_id {int} -- The pk of the computer being requested.

    Returns:
        render -- Returns the computer_detail template
    """
    computer = Computer.objects.get(pk=computer_id)
    computer_employee = EmployeeComputer.objects.filter(computer_id=computer_id)

    context = {
        "computer": computer,
        "computer_employee": computer_employee
    }

    return render(request, "agileHR/computer_detail.html", context)