# Finance Project API
## Run this commands to start project
>
### create env
> python -m venv env
>
> source env/bin/activate
### install requirements
> pip install -r requirements.txt
### create postgres database
> psql -U postgres
>
> create database dbname;
>
> create user dbuser;
>
> grant all on database dbname to dbuser;
>
> \password dbuser
### fill .env file based ion .env.template
### migrate 
> python manage.py migrate
### create admin user
> python manage.py createsuperuser
### run 
> python manage.py runserver 
### create api token 
- go to admin page (host/admin/);
- create API key into admin panel;
- remember the token
### set up telegram bot
[FinanceProjectApi](https://github.com/zhenerBY/FinanceProjectApi)