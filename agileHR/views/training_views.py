from datetime import datetime, date, timezone
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from agileHR.models import *

def training(request):
    """Displays the list of upcoming training sessions with links to details for each one.

    Author: Kelly Morin

    Returns:
        render -- Returns the training template
    """

    training_list = Training.objects.filter(end_date__date__gte=datetime.date.today()).order_by("start_date")

    context = {
        "training_list": training_list,
        "view": "upcoming"
    }

    return render(request, "agileHR/training.html", context)


def training_past(request):
    """Displays a list of all training sessions that have ended before today's date

    Author: Kelly Morin

    Returns:
        render -- returns the training template
    """

    training_list = Training.objects.filter(end_date__date__lt=datetime.date.today()).order_by("-start_date")

    context = {
        "training_list": training_list,
        "view": "past"
    }

    return render(request, "agileHR/training.html", context)


def training_detail(request, training_id):
    """Displays the details about a single training session hosted by the company

    Author: Kelly Morin

    Arguments:
        training_id {int} -- The pk of the training seession being requested

    Returns:
        render -- Returns the training_detail template
    """

    now = datetime.datetime.now(timezone.utc)
    training_details = get_object_or_404(Training, pk=training_id)
    attendee_size = len(EmployeeTraining.objects.filter(training_id=training_id))
    start_future = True
    end_future = True
    if training_details.start_date < now:
        start_future = False
    if training_details.end_date < now:
        end_future = False

    context = {
        "training_details": training_details,
        "attendee_size": attendee_size,
        "start_future": start_future,
        "end_future": end_future
    }

    return render(request, "agileHR/training_detail.html", context)


def training_edit(request, training_id):
    """Displays form to edit existing training session, handles all user interaction following POST request

    Author: Kelly Morin

    Arguments:
        training_id {int} -- The id of the training session the user is trying to edit

    Returns:
        render -- returns the training_form template, pre-populated with the existing training session data
        render -- returns the training_form template, pre-populated with the provided changes and error message to be displayed if form validation was incomplete
        render -- returns the training_details template with the updated session information
    """

    training_details = get_object_or_404(Training, pk=training_id)
    if request.method == "POST":

        try:
            title = request.POST["training_title"]
            start_date = request.POST["start_date"]
            end_date = request.POST["end_date"]
            max_attendees = request.POST["max_attendees"]

            if title is "" or start_date is "" or end_date is "" or max_attendees is "":

                # If start date or end date are the fields that are left blank upon submit, repopulate the form with the data currently in the database, otherwise create a datetime object from the string passed in by the form
                if start_date is "":
                    new_start_date = training_details.start_date
                    if end_date is "":
                        new_end_date = training_details.end_date
                    else:
                        new_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                elif end_date is "":
                    new_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                    new_end_date = training_details.end_date
                else:
                    new_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                    new_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

                context = {
                    "error_message": "You must complete all fields in the form",
                    "title": "Edit Training Session",
                    "form_detail": "edit",
                    "training_details": {
                        "id": training_id,
                        "title": title,
                        "start_date": new_start_date,
                        "end_date": new_end_date,
                        "max_attendees": max_attendees
                    }
                }
                return render(request, "agileHR/training_form.html", context)
            else:
                training_details.title = title
                training_details.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                training_details.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                training_details.max_attendees = max_attendees
                training_details.save()
                return HttpResponseRedirect(reverse("agileHR:traindetail", args=(training_id,)))
        except KeyError:
            return render(request, "agileHR/training_form.html", {
                "error_message": "You must complete all fields in the form",
                "title": "Edit Training Session",
                "form_detail": "edit",
                "training_details": training_details
            })
    else:
        context={
            "training_details": training_details,
            "title": "Edit Training Session" ,
            "form_detail": "edit"
        }

        return render(request, "agileHR/training_form.html", context)


def training_add(request):
    """Displays form to add a new training session, handles all user interaction following a post request

    Author: Kelly Morin

    Returns:
        render -- returns the training form template
        render -- returns the training_form template with an error message to be displayed if form validation was incomplete
        render -- returns the training template with the new training session added in it's appropriate place, sorted by start date
    """

    if request.method == "POST":

        try:
            title= request.POST["training_title"]
            start_date = request.POST["start_date"]
            end_date = request.POST["end_date"]
            max_attendees = request.POST["max_attendees"]

            if title is "" or start_date is "" or end_date is "" or max_attendees is "":
                return render(request, "agileHR/training_form.html", {
                    "error_message": "You must complete all fields in the form"
                })
            else:
                new_training = Training(title=title, start_date=start_date, end_date=end_date, max_attendees=max_attendees)
                new_training.save()
                return HttpResponseRedirect(reverse("agileHR:training"))
        except KeyError:
            return render(request, "agileHR/training_form.html", {
                "error_message": "You must complete all fields in the form"
            })
    else:
        context={
            "title": "Add New Training Session" ,
            "form_detail": "new"
        }
        return render(request, "agileHR/training_form.html", context)

def training_delete(request, training_id):
    """Deletes a future training - but not a past training

    Author: Brendan McCray

    Returns:
        render -- returns the training_delete template
    """

    if request.method == 'POST':
        training = Training.objects.get(pk=training_id)
        training.delete()
        return HttpResponseRedirect(reverse("agileHR:training"))
    else:
        training = Training.objects.get(pk=training_id)

        if training.start_date.date() > date.today():
            context = {
                "training": training,
                "can_delete": True
            }
        else:
            context = {
                "training": training,
                "can_delete": False
            }
        return render(request, 'agileHR/training_delete.html', context)