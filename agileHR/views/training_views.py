from datetime import datetime, date
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

    training_list = Training.objects.filter(start_date__date__gte=datetime.date.today()).order_by('start_date')
    context = {'training_list': training_list}
    return render(request, "agileHR/training.html", context)


def training_detail(request, training_id):
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

def training_edit(request, training_id):
    training_details = get_object_or_404(Training, pk=training_id)
    if request.method == 'POST':
        try:
            title = request.POST['training_title']
            start_date = request.POST["start_date"]
            end_date = request.POST['end_date']
            max_attendees = request.POST['max_attendees']
            if title is '' or start_date is '' or end_date is '' or max_attendees is '':
                # If start date or end date are the fields that are left blank upon submit, repopulate the form with the data currently in the database, otherwise create a datetime object from the string passed in by the form
                if start_date is '':
                    new_start_date = training_details.start_date
                    if end_date is '':
                        new_end_date = training_details.end_date
                    else:
                        new_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                elif end_date is '':
                    new_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                    new_end_date = training_details.end_date
                else:
                    new_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                    new_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

                context = {
                    'error_message': "You must complete all fields in the form",
                    'title': "Edit Training Session",
                    'form_detail': "edit",
                    'training_details': {
                        'id': training_id,
                        'title': title,
                        'start_date': new_start_date,
                        'end_date': new_end_date,
                        'max_attendees': max_attendees
                    }
                }
                return render(request, 'agileHR/training_form.html', context)
            else:
                training_details.title = title
                training_details.start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
                training_details.end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                training_details.max_attendees = max_attendees
                training_details.save()
                return HttpResponseRedirect(reverse("agileHR:traindetail", args=(training_id,)))
        except KeyError:
            return render(request, "agileHR/training_form.html", {
                'error_message': "You must complete all fields in the form",
                'title': "Edit Training Session",
                'form_detail': "edit", 'training_details': training_details})
    else:
        context={'training_details': training_details, 'title': "Edit Training Session" , 'form_detail': "edit" }
        return render(request, 'agileHR/training_form.html', context)

def training_add(request):
    """Displays form to add a new training session

    Author: Kelly Morin

    Returns:
        render -- returns the training form template, an error message to be displayed or the training template with the new training session added
    """

    if request.method == 'POST':
        try:
            title= request.POST['training_title']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            max_attendees = request.POST['max_attendees']
            if title == '' or start_date == '' or end_date == '' or max_attendees == '':
                return render(request, 'agileHR/training_form.html', {'error_message': "You must complete all fields in the form"})
            else:
                new_training = Training(title=title, start_date=start_date, end_date=end_date, max_attendees=max_attendees)
                new_training.save()
                return HttpResponseRedirect(reverse('agileHR:training'))
        except KeyError:
            return render(request, 'agileHR/training_form.html', {'error_message': "You must complete all fields in the form"})
    else:
        context={'title': "Add New Training Session" , 'form_detail': "new"}
        return render(request, 'agileHR/training_form.html', context)

def training_delete(request, training_id):
    if request.method == 'POST':
        training = Training.objects.get(pk=training_id)
        training.delete()
        return HttpResponseRedirect(reverse("agileHR:training"))
    else:
        training = Training.objects.get(pk=training_id)

        if training.end_date.date() > date.today():
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