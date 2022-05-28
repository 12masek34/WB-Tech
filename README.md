OpenAPI doc at
```commandline
http://localhost:8000/docs/
```

## deployment.

###  docker.
```commandline
$  chmod +x ./entrypoint.sh
```
```commandline
$ docker-compose up -d --build
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
### Run tests.
```commandline
 $ python manage.py test
```