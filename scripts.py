import os
import sys


def runserver():
    os.system('python manage.py runserver')


def migrate():
    os.system('python manage.py migrate')


def startapp():
    try:
        app_name = sys.argv[1]
        os.system(f'python manage.py startapp {app_name}')
    except BaseException:
        print('Need set name of app. Example: "poetry run startapp blog"')


def makemigrations():
    cmd = 'python manage.py makemigrations'
    if len(sys.argv) > 1:
        cmd = cmd + ' ' + ' '.join(sys.argv[1:]) 
    os.system(cmd)


def requirements():
    os.system('poetry export -f requirements.txt --output requirements.txt')


def createsuperuser():
    os.system('python manage.py createsuperuser')


def collectstatic():
    os.system('python manage.py collectstatic')
