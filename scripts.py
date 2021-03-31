import os
import sys
import platform


def shell_run(command: str):
    if platform.system() == 'Windows':
        cmd = f'cd controle_financeiro & {command}'
    else:
        cmd = f'cd ./controle_financeiro && {command}'
    os.system(cmd)


def runserver():
    shell_run('python manage.py runserver')


def test():
    shell_run('pytest')


def migrate():
    shell_run('python manage.py migrate')


def startapp():
    try:
        app_name = sys.argv[1]
        shell_run(f'python manage.py startapp {app_name}')
    except BaseException:
        print('Need set name of app. Example: "poetry run startapp blog"')


def makemigrations():
    cmd = 'python manage.py makemigrations'
    if len(sys.argv) > 1:
        cmd = cmd + ' ' + ' '.join(sys.argv[1:])
    shell_run(cmd)


def requirements():
    os.system('poetry export -f requirements.txt --output requirements.txt')


def createsuperuser():
    shell_run('python manage.py createsuperuser')


def collectstatic():
    shell_run('python manage.py collectstatic')
