# Django project


1. Install django and it's dependencies
```bash
pip install django
pip install whitenoise  # for Static files
pip install psycopg2-binary  # for PostgreSQL
```

2. Create project
```bash
django-admin startproject my_club
```

3. Create App
```bash
python manage.py startapp members
```

4. Run the project
```bash
python manage.py runserver
```

5. Migrate
```bash
python manage.py makemigrations members
```

6. Admin
```bash
python manage.py createsuperuser
```

7. Use PostgreSQL database
https://hub.docker.com/_/postgres

```bash
docker run -p 5432:5432 --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
```
