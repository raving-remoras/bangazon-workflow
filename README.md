# Bangazon-Workflow

## Installation
- Create an empty directory to house your new project
- `virtualenv env` to create a virtual environment within that directory
- `source env/bin/activate` to run virtual environment (`deactivate` to exit environment)
- `git clone [repository id]`
- `cd bangazon-workflow`
- `pip install -r requirements.txt`

## Using the Application

### Seed a Starter Database
- run `python manage.py makemigrations agileHR`
- run `python manage.py migrate`
- If you want some data to play with run `python manage.py seeder`

- Initialize the project using the command line by typing `python manage.py runserver` in the main directory.
- Access the application in a browser at `http://localhost:8000/bangazon`.
- A navbar at the top of the page can be used to visit each of Bangazon's four Human Resources focus areas (employees, departments, trainings, and computers).

## Employees


## Departments


## Trainings


## Computers
