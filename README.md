## WB-Tech

This is a test task for creating a blog api.<br>

Technical specification of the project in the file task.pdf

---
OpenAPI doc at
```commandline
http://localhost:8000/docs/
```
or in file openapi.yml.

---
## deployment.

###  docker.
```commandline
$  chmod +x ./entrypoint.sh
```
```commandline
$ docker-compose up -d --build
```
Create superuser in docker container.
```commandline
$ docker exec -it wb_tech_web_1 python manage.py createsuperuser

```
Run tests in docker container.
```commandline
$ docker exec -it wb_tech_web_1 python manage.py test

```
### manual.

Run local postgres server 127.0.0.1:5432.<br>

```
$ python -m venv venv
```
```
$ source venv/bin/activate
```
```
$ pip install -r requirements.txt
```
```
$ python manage.py makemigrations
```
```
$ python manage.py migrate
```
```
$ python manage.py runserver
```
Create superuser.
```commandline
$ python manage.py createsuperuser
```
Run tests.
```commandline
 $ python manage.py test
```