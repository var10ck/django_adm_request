# Django ADM requests
## Requirements
This project has only one requirement:
 - Python 3.6+
## Installation
After cloning this repository you'll need to install all requirements using pip:

`pip install -r requirements.txt`

Optionally you can configure database settings in django_adm_request/settings.py. By default app using sqlite.
Then you need to execute following commands from terminal:

`python manage.py makemigrations`

`python manage.py migrate`

This commands will generate database schema. 
Create admin-account by executing:

`python manage.py createsuperuser`

Now you need to start the server:

`python manage.py runserver 8080`

The server will start listening port 8080. 
Open http://127.0.0.1:8080/ in your browser and use credentials of created superuser