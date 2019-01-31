from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from agileHR.models import *


def computers(request):
    """Displays the list of computers currently owned by the company with links to details for each one.

    Author: Sebastian Civarolo

    Returns:
        render -- loads the computer.html template.
    """

    computers = Computer.objects.all().order_by("make", "model")
    context = {
        "computers": computers
    }
    return render(request, 'agileHR/computers.html', context)


def computer_search(request):

    if request.method == "POST":


        search_text = request.POST["search_text"]

        if search_text is not "":
            by_make = Computer.objects.filter(make__contains=search_text).order_by("make", "model")
            by_model = Computer.objects.filter(model__contains=search_text).order_by("make", "model")
            results = by_make | by_model
            context = {
                "results": results,
                "length": len(results),
                "search_text": search_text,
                "no_results": True if len(results) is 0 else False
            }
        else:
            context = {
                "no_results": True,
                "search_text": search_text
            }
        return render(request, 'agileHR/computer_search.html', context)

    else:
        return HttpResponseRedirect(reverse('agileHR:computers'))

def computer_detail(request, computer_id):
    """Displays the details about a single computer owned by the company.

    Arguments:
        computer_id {int} -- The pk of the computer being requested.

    Returns:
        render -- Returns the computer_detail template
    """

    computer = get_object_or_404(Computer, pk=computer_id)
    current_assignment = EmployeeComputer.objects.filter(computer_id=computer_id).filter(date_revoked=None)
    assignment_history = EmployeeComputer.objects.filter(computer_id=computer_id).exclude(date_revoked=None).order_by('-date_assigned')

    context = {
        "computer": computer,
        "current_assignment": current_assignment,
        "assignment_history": assignment_history
    }

    return render(request, "agileHR/computer_detail.html", context)


def new_computer(request):
    """Displays the form to add a new computer, and checks for all inputs before saving to the database.

    Author: Sebastian Civarolo

    Returns:
        render -- Returns the form with an error message, or if successful, returns the new detail page.
        HttpResponseRedirect -- when request is POST, will send you to the detail page if the computer creation is successfull.
    """

    if request.method == "POST":

        try:
            make = request.POST["make"]
            model = request.POST["model"]
            serial_no = request.POST["serial_no"]
            purchase_date = request.POST["purchase_date"]
            employee_id = request.POST["employee"]
            employee = Employee.objects.get(pk=employee_id)

            if make is "" or model is "" or serial_no is "" or purchase_date is "":
                return render(request, "agileHR/computer_new.html", {
                    "error_message": "Please fill out all fields",
                    "make": make,
                    "model": model,
                    "serial_no": serial_no,
                    "purchase_date": purchase_date
                })
            else:
                now = datetime.datetime.now()
                new_computer = Computer(make=make, model=model, serial_no=serial_no, purchase_date=purchase_date)
                new_computer.save()
                join = EmployeeComputer.objects.create(
                    computer = new_computer,
                    employee = employee,
                    date_assigned = now
                )
                join.save()

                return HttpResponseRedirect(reverse("agileHR:computer_detail", args=(new_computer.id,)))
        except KeyError:
            return render(request, "agileHR/computer_new.html", {
                "error_message": "Please fill out all fields"
            })
    else:
        # Get all computer assignment history
        computer_assignments = EmployeeComputer.objects.all()

        # Get employees who have had a computer but do not currently have one.
        need_computers = Employee.objects.exclude(employeecomputer__date_revoked=None).order_by('last_name')

        # Get employees who have never had a computer.
        never_computers = Employee.objects.exclude(employeecomputer__in=computer_assignments).order_by('last_name')

        # Combine the two querysets
        final_list = need_computers | never_computers

        context = {
            "employees": final_list
        }

        return render(request, "agileHR/computer_new.html", context)


def delete_computer(request, computer_id):
    """Deletes a computer ONLY if it has NEVER been assigned to an employee.

        Author: Sebastian Civarolo

        Arguments:
            computer_id {int} -- the ID of the computer to be deleted.

        Returns:
            render -- loads the delete confirmation view with corresponding message.
            HttpResponseRedirect -- when request is POST, will delete the computer and redirect to the computers view.
    """

    if request.method == "POST":
        computer = Computer.objects.get(pk=computer_id)
        computer.delete()
        return HttpResponseRedirect(reverse("agileHR:computers"))

    else:
        computer = Computer.objects.get(pk=computer_id)
        assignments = EmployeeComputer.objects.filter(computer_id=computer_id)

        if len(assignments) == 0:
            context = {
                "computer": computer,
                "can_delete": True
            }
        else :
            context = {
                "computer": computer,
                "can_delete": False
            }
        return render(request, "agileHR/computer_delete.html", context)