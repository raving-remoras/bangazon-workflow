import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import *

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
    """This method queries the database for department and related employee information and renders the department template.

    Author: Brendan McCray

    Returns:
        render -- loads the department.html template.
    """

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

def department_detail(request, dept_id):
    """This method queries the database for a specific department and its employee information and renders the department_detail template.

    Author: Brendan McCray

    Returns:
        render -- loads the department_detail.html template.
    """

    department = get_object_or_404(Department, pk=dept_id)
    try:
        employees = Employee.objects.filter(department_id=dept_id)
        context = {"department": department, "employees": employees}
    except Employee.DoesNotExist:
        context = {"department": department}
    return render(request, 'agileHR/department_detail.html', context)

def training(request):
    """Displays the list of upcoming training sessions with links to details for each one.

    Author: Kelly Morin

    Returns:
        render -- Returns the training template
    """

    training_list = Training.objects.filter(start_date__date__gte=datetime.date.today()).order_by('start_date')
    context = {'training_list': training_list}
    return render(request, "agileHR/training.html", context)


def traindetail(request, training_id):
    """Displays the details about a single training session hosted by the company

    Author: Kelly Morin

    Arguments:
        training_id {int} -- The pk of the training seession being requested

    Returns:
        render -- Returns the training_detail template
    """

    training_details = get_object_or_404(Training, pk=training_id)
    attendee_size = len(EmployeeTraining.objects.filter(training_id=training_id))
    context = {'training_details': training_details, 'attendee_size': attendee_size}
    return render(request, 'agileHR/training_detail.html', context)


def computers(request):
    """Displays the list of computers currently owned by the company with links to details for each one.

    Author: Sebastian Civarolo

    Returns:
        render -- loads the computer.html template.
    """

    computers = Computer.objects.all()
    context = {
        "computers": computers
    }
    return render(request, 'agileHR/computers.html', context)


def computer_detail(request, computer_id):
    """Displays the details about a single computer owned by the company.

    Arguments:
        computer_id {int} -- The pk of the computer being requested.

    Returns:
        render -- Returns the computer_detail template
    """

    computer = get_object_or_404(Computer, pk=computer_id)

    context = {
        "computer": computer
    }

    return render(request, "agileHR/computer_detail.html", context)


def new_computer(request):
    """Displays the form to add a new computer, and checks for all inputs before saving to the database.

    Author: Sebastian Civarolo

    Returns:
        render -- Returns the form with an error message, or if successful, returns the new detail page.
    """

    if request.method == "POST":
        print("REQUEST", request.POST)
        try:
            make = request.POST["make"]
            model = request.POST["model"]
            serial_no = request.POST["serial_no"]
            purchase_date = datetime.datetime.now()

            if make is "" or model is "" or serial_no is "":
                return render(request, "agileHR/computer_new.html", {
                    "error_message": "Please fill out all fields"
                })
            else:
                new_computer = Computer(make=make, model=model, serial_no=serial_no, purchase_date=purchase_date)
                new_computer.save()
                return HttpResponseRedirect(reverse("agileHR:computer_detail", args=(new_computer.id,)))
        except KeyError:
            return render(request, "agileHR/computer_new.html", {
                "error_message": "Please fill out all fields"
            })
    else:
        context = {}
        return render(request, "agileHR/computer_new.html", context)
