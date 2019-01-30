# Bangazon-Workflow

## Installation
- Create an empty directory to house your new project
- run `virtualenv env` to create a virtual environment within that directory
- run `source env/bin/activate` to initialize a virtual environment (`deactivate` to exit environment)
- run `git clone [repository id]`
- run `cd bangazon-workflow`
- run `pip install -r requirements.txt`

## Seed a Starter Database
- Run `python manage.py makemigrations agileHR`
- Run `python manage.py migrate`
- If you want some data to play with, run `python manage.py seeder`
- Initialize the project using the command line by typing `python manage.py runserver` in the main directory.
- Access the application in a browser at `http://localhost:8000/bangazon`.
- A navbar at the top of the page can be used to visit each of Bangazon's four Human Resources focus areas (employees, departments, trainings, and computers).

## Employees


## Departments
- Departments can be accessed via the navbar. A list of all departments' titles, budgets, and sizes (number of assigned employees) is visible.
- Clicking on a department will display a list of all assigned employees' names. The user can return to the departments list by clicking <em>Go Back</em>
- Clicking <em>Add a New Department</em> will open a form that prompts the user to submit a new department name and budget. Saving the form data will return the user to the list of departments. The user can find the department in the list alphabetically.
- Alternatively, the user can click <em>Go Back</em> to return to the departments list without saving new data.

## Trainings
- Training sessions can be accessed via the navbar. A list of all training sessions' titles and start date is visible.
- Clicking <em>Add New Training</em> will open a form that prompts the user to submit a new training session title, start and end date and maximum number of attendees. Saving the session will return the user to the list of training sesssions. The user can find their training session in the list sorted by date.
- Alternatively, the user can click <em>Go Back</em> to return to the training session list without saving new data.
- Clicking on a training session will display the training sessions title, start and end date, maximum number of attendees, available seats as well as a list of all employees that are currently registered for that session. The user can return to the training session list by clicking <em>View all Training Sessions</em>.
- The user can click <em>Edit Details</em> button to be taken to a form that allows the user to edit the details of the training session. Upon saving the session, the user will be returned to the updated training session detail page where their changes will be displayed.
- Alternatively, the user can select <em>Go Back</em> to return to the training session list without saving changes.


## Computers
