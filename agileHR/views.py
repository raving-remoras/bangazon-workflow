import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Employee, Department, Training, Computer, EmployeeTraining

def index(request):
    context = {}
    return render(request, "agileHR/index.html", context)

def employee(request):
    employee_list = Employee.objects.all()
    context = {'employee_list': employee_list}
    return render(request, 'agileHR/employee.html', context)

def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    context = {'employee': employee}
    return render(request, 'agileHR/employee_detail.html', context)

def department(request):
    departments = Department.objects.all()
    employees = Employee.objects.all()
    dept_size = Employee.objects.raw("""SELECT COUNT(agileHR_employee.department_id) AS "count", agileHR_department.id
        FROM agileHR_employee
        JOIN agileHR_department WHERE agileHR_department.id = agileHR_employee.department_id
        GROUP BY department_id"""
    )

    context = {
        "departments": departments,
        "employees": employees,
        "dept_size": dept_size
    }
    return render(request, "agileHR/department.html", context)

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
