from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from agileHR.models import *


def department(request):
    """This method queries the database for department and related employee information and renders the department template.

    Author: Brendan McCray

    Returns:
        render -- loads the department.html template.
    """

    departments = Department.objects.all().order_by("name")
    dept_size = Employee.objects.raw("""SELECT COUNT(agileHR_employee.department_id) AS "count", agileHR_department.id
        FROM agileHR_employee
        JOIN agileHR_department WHERE agileHR_department.id = agileHR_employee.department_id
        GROUP BY department_id"""
    )

    context = {
        "departments": departments,
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
        employees = Employee.objects.filter(department_id=dept_id).order_by("last_name")
        context = {"department": department, "employees": employees}
    except Employee.DoesNotExist:
        context = {"department": department}
    return render(request, 'agileHR/department_detail.html', context)

def departmentadd(request):
    """This method loads a form to add a new department, and, if the form is filled out completely, will then redirect to the departments list

    Author: Brendan McCray

    Returns:
        render -- loads the department_form.html template.
        HttpResponseRedirect -- loads the list of all departments
    """

    if request.method == "POST":
        try:
          name = request.POST["dept_name"]
          budget = request.POST["dept_budget"]
          if name == "" or budget == "":
            return render(request, "agileHR/department_form.html", {
              "error_message": "You must complete all fields in the form.",
              "name": name,
              "budget": budget
              })
          else:
            new_dept = Department(name=name.lower(), budget=budget)
            new_dept.save()
            return HttpResponseRedirect(reverse("agileHR:department"))
        except KeyError:
          return render(request, "agileHR/department_form.html", {
            "error_message": "You must complete all fields in the form."
            })
    # if navigating through this method, only the form is loaded (no post in request)
    else:
      context = {}
      return render(request, 'agileHR/department_form.html', context)
