import os
import sys
import platform
from typing import List, Union


def shell_run(command: Union[str, List[str]]):
    and_ = ' & ' if platform.system() == 'Windows' else ' && '
    folder = 'cd controle_financeiro'
    args_cmd = and_.join(command if isinstance(command, list) else [command])
    final_cmd = folder + and_ + args_cmd
    print(args_cmd)
    os.system(final_cmd)


def runserver():
    shell_run('python manage.py runserver')


def test():
    shell_run('python manage.py test')


def lint():
    shell_run(['flake8 .', 'mypy .'])


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


def djangoshell():
    shell_run('python manage.py shell')


def dbshell():
    cmd = 'python manage.py dbshell'
    if len(sys.argv) > 1:
        cmd = cmd + f" '{sys.argv[1]}'"
    shell_run(cmd)
