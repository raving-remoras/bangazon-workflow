import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.db import connection
from agileHR.models import *


def employee(request):
    """This method queries the database for all employees ordered by last name and renders the employee page

    Author: Rachel Daniel

    Returns:
        render -- loads the employee.html template.
    """
    sql = """
            SELECT * FROM agileHR_employee E
            ORDER BY E.last_name
        """
    employee_list = Employee.objects.raw(sql)
    context = {'employee_list': employee_list}
    return render(request, 'agileHR/employee.html', context)


def employee_detail(request, employee_id):
    """This method queries the database for the employee clicked on employee page as well as their current (non-revoked) computer, and renders the employee detail page

    Author: Rachel Daniel

    Returns:
        render -- loads the employee_detail.html template.
    """
    employee_sql = """
            SELECT * FROM agileHR_employee E
            WHERE E.id = %s
        """
    emp_comp_sql = """
            SELECT * FROM agileHR_employeecomputer EC
            WHERE EC.id = %s
            AND EC.date_revoked is NULL
        """

    employee = Employee.objects.raw(employee_sql, [employee_id])[0]
    employee_computer = EmployeeComputer.objects.raw(employee_sql, [employee_id])
    context = {"employee": employee, "employee_computer": employee_computer}
    return render(request, "agileHR/employee_detail.html", context)


def employee_add(request):
    """This method queries the database for the departments and renders the form for adding a new employee. Upon submit, the method collects form data from post request, validates, and adds a new employee

    Author: Rachel Daniel

    Returns:
        render -- loads the employee_form.html template with add context when originally navigating to the page, or renders form with error message if submit was unsuccessful
        HttpResponseRedirect -- loads the employee page if add was successful
    """

    sql = """
        SELECT * FROM agileHR_department D
        ORDER BY D.name
    """

    departments = Department.objects.raw(sql)

    if request.method == "POST":
        try:
            department = request.POST["department"]
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
                sql = "INSERT into agileHR_employee VALUES (%s, %s, %s, %s, %s, %s, %s)"
                with connection.cursor() as cursor:
                    cursor.execute(sql,[None, first_name, last_name, start_date, None, is_supervisor, department])
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

    depts_sql = """
        SELECT * FROM agileHR_department D
        ORDER BY D.name
    """

    employee_sql = """
        SELECT * FROM agileHR_employee E
        WHERE E.id = %s
    """
    emp_comp_sql = """
        SELECT * FROM agileHR_employeecomputer EC
        WHERE EC.id = %s
        AND EC.date_revoked = NULL
    """
    trainings_sql = """
        SELECT * FROM agileHR_training T
        WHERE t.start_date >= %s
        ORDER BY t.start_date
    """
    emp_trainings_sql = """
        SELECT * FROM agileHR_training T
        JOIN agileHR_employeetraining ET
        ON T.id = ET.training_id
        WHERE T.start_date >= %s
        AND ET.employee_id = %s
    """
    computer_sql = """
        SELECT * FROM agileHR_computer C
        LEFT JOIN agileHR_employeecomputer EC
        ON C.id = EC.computer_id
        WHERE EC.date_revoked is null
        OR EC.id is null
    """

    departments = Department.objects.raw(depts_sql)
    employee = Employee.objects.raw(employee_sql, [employee_id])[0]
    employee_computer = EmployeeComputer.objects.raw(employee_sql, [employee_id])
    trainings = Training.objects.raw(trainings_sql, [now])
    employee_trainings = EmployeeTraining.objects.raw(emp_trainings_sql, [now, employee_id])
    computers = Computer.objects.raw(computer_sql)

    if request.method == "POST":

        try:
            department = request.POST["department"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            start_date = request.POST["start_date"] + " 00:00:00"
            end_date = request.POST["end_date"] + " 00:00:00"
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
                    "start_date": employee.start_date,
                    "end_date": employee.end_date,
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
                            sql = "UPDATE agileHR_employeecomputer SET date_revoked = %s WHERE id = %s"
                            with connection.cursor() as cursor:
                                cursor.execute(sql, [now, assignment.id])
                    new_comp_sql = """
                        SELECT * FROM agileHR_computer C
                        WHERE C.id = %s
                    """
                    join_sql = "INSERT INTO agileHR_employeecomputer VALUES (%s, %s, %s, %s, %s)"
                    with connection.cursor() as cursor:
                        cursor.execute(join_sql, [None, now, None, __comp, employee.id])

                # delete any upcoming trainings with delete boxes checked
                for training in delete_training_set:
                    with connection.cursor() as cursor:
                        cursor.execute("DELETE FROM agileHR_employeetraining WHERE id = %s", [training])

                # add a join entity to EmployeeTraining for every upcoming training selected
                for training in add_training_set:
                    join_sql = "INSERT INTO agileHR_employeetraining VALUES (%s, %s, %s)"
                    with connection.cursor() as cursor:
                        cursor.execute(join_sql, [None, employee.id, training])

                #update employee entity with any altered info
                with connection.cursor() as cursor:
                    emp_edit_sql = """
                        UPDATE agileHR_employee
                        SET first_name=%s, last_name=%s, department_id=%s, is_supervisor=%s, start_date=%s, end_date=%s
                        WHERE id=%s
                    """
                    cursor.execute(emp_edit_sql, [first_name, last_name, department, is_supervisor, start_date, end_date, employee.id])

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
            "start_date": employee.start_date,
            "end_date": employee.end_date,
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
            "start_date": employee.start_date,
            "end_date": employee.end_date,
            "is_supervisor": employee.is_supervisor,
            "department": employee.department
            }
        print("employee_computer", context["employee_computer"])
        return render(request, "agileHR/employee_form.html", context)
