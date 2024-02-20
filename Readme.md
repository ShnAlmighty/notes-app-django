# Note Taking Backend

## Information
This is a simple note-taking application RESTful API built using Django and Django REST Framework. It allows users to perform CRUD operations (Create, Read, Update, Delete) on notes, as well as manage user authentication and authorization.

## Setup Instructions
 1. Install the dependencies by running the below commands from the project's root directory in the command line:
```bash
$pip3 install requirements.txt
```
 or

 You can also use a virtual evnironement first to isolate the project's dependencies:
```bash
$python3 -m venv env
$source env/bin/activate
(env)$pip3 install requirements.txt
```

 2. Setup Database, the project uses SQLite as the database engine by default. The database can be setup by running the following commands (also creates the super user for Django administrative privileges):
```bash
$python3 notesapp/manage.py makemigrations
$python3 notesapp/manage.py migrate
$python3 notesapp/manage.py createsuperuser
```

## Starting the Server
To start the server:
```bash
$python3 notesapp/manage.py runserver
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.