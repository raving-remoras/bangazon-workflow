import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from agileHR.models import *


def employee(request):
    """This method queries the database for all employees ordered by last name and renders the employee page

    Author: Rachel Daniel

    Returns:
        render -- loads the employee.html template.
    """
    employee_list = Employee.objects.order_by('last_name')
    context = {'employee_list': employee_list}
    return render(request, 'agileHR/employee.html', context)

def employee_detail(request, employee_id):
    """This method queries the database for the employee clicked on employee page as well as their current (non-revoked) computer, and renders the employee detail page

    Author: Rachel Daniel

    Returns:
        render -- loads the employee_detail.html template.
    """
    employee = get_object_or_404(Employee, pk=employee_id)
    employee_computer = EmployeeComputer.objects.filter(employee_id=employee_id).filter(date_revoked=None)
    context = {"employee": employee, "employee_computer": employee_computer}
    return render(request, "agileHR/employee_detail.html", context)


def employee_add(request):
    """This method queries the database for the departments and renders the form for adding a new employee. Upon submit, the method collects form data from post request, validates, and adds a new employee

    Author: Rachel Daniel

    Returns:
        render -- loads the employee_form.html template with add context when originally navigating to the page, or renders form with error message if submit was unsuccessful
        HttpResponseRedirect -- loads the employee page if add was successful
    """
    departments = Department.objects.order_by('name')

    if request.method == "POST":
        try:
            department = get_object_or_404(Department, pk=request.POST["department"])
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            start_date = request.POST["start_date"]
            is_supervisor = (request.POST.get("is_supervisor", "") == "on")
            if first_name == "" or last_name == "" or start_date == "":
                return render(request, "agileHR/employee_form.html", {"error_message": "You must complete all fields in the form.", "departments": departments,
                "first_name": first_name,
                "last_name": last_name,
                "start_date": start_date,
                "department": department,
                "is_supervisor": is_supervisor,
                "add":"add"
                })

            else:
                new_employee = Employee(first_name=first_name, last_name=last_name, department=department, is_supervisor=is_supervisor, start_date=start_date)
                new_employee.save()
                messages.success(request, 'Saved!')
                return HttpResponseRedirect(reverse("agileHR:employee"))


        except KeyError:
            return render(request, 'agileHR/employee_form.html', {
            'error_message': "You must complete all fields in the form.", "departments": departments, "add":"add"
            })
    else:

        context = {"departments": departments, "add":"add"}
        return render(request, "agileHR/employee_form.html", context)


def employee_edit(request, employee_id):
    """This method queries the database for the departments, unassigned computers, upcoming trainings, current employee and their assigned computer, loads an edit form, and allows users to update Employee, EmployeeComputer and EmployeeTraining

    Author: Rachel Daniel

    Returns:
        render -- loads the employee_form.html template with edit context when originally navigating to the page, or renders form with error message if submit was unsuccessful
        HttpResponseRedirect -- loads the employee page if edit was successful
    """
    now = datetime.datetime.now()
    departments = Department.objects.order_by("name")
    employee = get_object_or_404(Employee, pk=employee_id)
    employee_computer = EmployeeComputer.objects.filter(employee_id=employee_id, date_revoked=None)
    trainings = Training.objects.filter(start_date__gt=now).order_by("start_date")
    employee_trainings = EmployeeTraining.objects.filter(employee_id=employee_id, training__start_date__gt=now)


    # Get all computer assignment history
    computer_assignments = EmployeeComputer.objects.all()

    # Get computers that have previously been assigned but currently aren't
    currently_unassigned = Computer.objects.exclude(employeecomputer__date_revoked=None)

    # Get computers that have never been assigned
    never_assigned = Computer.objects.exclude(employeecomputer__in=computer_assignments)

    #combine queryset for final set of available computers
    computers = currently_unassigned | never_assigned

    if request.method == "POST":

        try:
            department = get_object_or_404(Department, pk=request.POST["department"])
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            start_date = request.POST["start_date"]
            end_date = request.POST["end_date"]
            is_supervisor = request.POST.get("is_supervisor", "") == "on"
            __comp = request.POST["computer"]
            delete_training_set = request.POST.getlist("delete")
            add_training_set = request.POST.getlist("trainings")

            # check to make sure mandatory info is populated
            if first_name == "" or last_name == "" or start_date == "":
                context = {
                    "employee": employee,
                    "computers": computers,
                    "employee_computer": employee_computer,
                    "employee_trainings": employee_trainings,
                    "trainings": trainings,
                    "departments": departments,
                    "edit": "edit",
                    "first_name": employee.first_name,
                    "last_name": employee.last_name,
                    "start_date": employee.start_date.date(),
                    "end_date": employee.end_date.date(),
                    "is_supervisor": employee.is_supervisor,
                    "department": employee.department,
                    "error_message": "You must complete all required fields."
                }
                return render(request, "agileHR/employee_form.html", context)
            else:

                # check for new computer assignment-- if new comp, unassign any old comps and create join enitity for new
                if __comp != "select":
                    if employee_computer:
                        for assignment in employee_computer:
                            assignment.date_revoked = now
                            assignment.save()
                    new_computer = get_object_or_404(Computer, pk=__comp)
                    join = EmployeeComputer(computer=new_computer, employee=employee, date_assigned=now)
                    join.save()
                    employee.employeecomputer_set.add(join)

                # delete any upcoming trainings with delete boxes checked
                for training in delete_training_set:
                    employee_training = EmployeeTraining.objects.get(pk=training)
                    employee_training.delete()

                # add a join entity to EmployeeTraining for every upcoming training selected
                for training in add_training_set:
                    new_training = get_object_or_404(Training, pk=training)
                    join = EmployeeTraining(employee=employee, training=new_training)
                    join.save()
                    employee.employeetraining_set.add(join)


                #update employee entity with any altered info
                employee.first_name = first_name
                employee.last_name = last_name
                employee.department = department
                employee.is_supervisor = is_supervisor
                employee.start_date = start_date
                if end_date != "":
                    employee.end_date = end_date
                employee.save()
                messages.success(request, 'Saved!')
                return HttpResponseRedirect(reverse("agileHR:employee"))


        except KeyError:
            context = {
            "employee": employee,
            "computers": computers,
            "employee_computer": employee_computer,
            "employee_trainings": employee_trainings,
            "trainings": trainings,
            "departments": departments,
            "edit": "edit",
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "start_date": employee.start_date.date(),
            "end_date": employee.end_date.date(),
            "is_supervisor": employee.is_supervisor,
            "department": employee.department,
            "error_message": "You must complete all required fields."
            }
            return render(request, 'agileHR/employee_form.html', context)
    else:
        #render initial edit page with populated data
        context = {
            "employee": employee,
            "computers": computers,
            "employee_computer": employee_computer,
            "employee_trainings": employee_trainings,
            "trainings": trainings,
            "departments": departments,
            "edit": "edit",
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "start_date": employee.start_date.date(),
            "end_date": employee.end_date.date(),
            "is_supervisor": employee.is_supervisor,
            "department": employee.department
            }
        print("employee_computer", context["employee_computer"])
        return render(request, "agileHR/employee_form.html", context)
