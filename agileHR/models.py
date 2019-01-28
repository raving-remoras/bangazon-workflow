import datetime
from django.db import models
from django.utils import timezone

"""Models component sets up data structure for agileHR app"""


class Department(models.Model):
    """Defines a department within the organization.

    Author: Brendan
    Returns:
        str -- Description of the employee and training relationship

    """

    name = models.CharField(max_length=100)
    budget = models.IntegerField()

    def __str__(self):
        return self.name


class Employee(models.Model):
    """Defines a past or present employee of the organization.

    Author: Rachel Daniel
    Returns:
        __str__ -- Full name, start and end date, and department
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    is_supervisor = models.BooleanField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Full Name: {self.first_name} {self.last_name} Start Date: {self.start_date} End Date: {self.end_date} Department: {self.department}"


class Training(models.Model):
    """Defines a class representing a training session being hosted by the company.

        Author: Kelly Morin

        Returns:
            str -- Training title, start and end date and maximum number of attendees
    """
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_attendees = models.IntegerField()

    def __str__(self):
        return f"{self.title} training session is scheduled for {self.start_date} and ends {self.end_date}. It can hold a maximum of {self.max_attendees} attendees"


class Computer(models.Model):
    """Defines a class representing a computer purchased by the company.

        Author: Sebastian Civarolo

        Returns:
            str -- Make, Model and Serial No. of a computer
    """

    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_no = models.CharField(max_length=100)
    purchase_date = models.DateTimeField()
    retire_date = models.DateTimeField(default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.make} {self.model} - Serial No: {self.serial_no}"


class EmployeeComputer(models.Model):
    """Defines the assignment of a computer to an employee and records the start and end dates.

        Author: Sebastian Civarolo

        Returns:
            str -- Employee name and Make, Model, and Serial No. of computer assigned to them.
    """

    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    computer = models.ForeignKey(Computer, on_delete=models.PROTECT)
    date_assigned = models.DateTimeField()
    date_revoked = models.DateTimeField()

    def __str__(self):
        return f"{self.employee.name}: {self.computer.make} {self.computer.model}, Serial No: {self.computer.serial_no}"


class EmployeeTraining(models.Model):
    """Defines a class representing a relationship between the employee and training sessions.

        Author: Kelly Morin

        Returns:
            str -- Description of the employee and training relationship
     """
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    training = models.ForeignKey(Training, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.employee} is registered for {self.training}"