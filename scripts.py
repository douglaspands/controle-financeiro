import os
import platform
import re
import sys
from typing import List, Union


def get_app_basename() -> str:
    app_basename = re.sub(r"[\s-]", "_", os.path.basename(os.getcwd()).lower())
    return app_basename


def get_app_path() -> str:
    app_path = os.path.join(os.getcwd(), get_app_basename())
    return app_path


def shell_run(command: Union[str, List[str]]):
    and_ = " & " if platform.system() == "Windows" else " && "
    folder = f"cd {get_app_path()}"
    args_cmd = and_.join(command if isinstance(command, list) else [command])
    final_cmd = folder + and_ + args_cmd
    print(args_cmd)
    os.system(final_cmd)


def runserver():
    shell_run("python manage.py runserver")


def test(accept_args=True):
    cmd = (
        "coverage run "
        "--omit=*/venv/*,*/migrations/*,*/tests/*,*/settings/* "
        f"--source='.' manage.py test --settings={get_app_basename()}.settings.test"
    )
    if accept_args is True:
        if len(sys.argv) > 1:
            cmd = cmd + " " + " ".join(sys.argv[1:])
    shell_run(cmd)


def coverage():
    cmd = "coverage report -m"
    shell_run(cmd)
    cmd = "coverage html"
    shell_run(cmd)


def testcov():
    test(accept_args=False)
    coverage()


def lint():
    shell_run(["flake8 .", "mypy ."])


def migrate():
    shell_run("python manage.py migrate")


def startapp():
    try:
        app_name = sys.argv[1]
        shell_run(f"python manage.py startapp {app_name}")
    except BaseException:
        print('Need set name of app. Example: "poetry run startapp blog"')


def makemigrations():
    cmd = "python manage.py makemigrations"
    if len(sys.argv) > 1:
        cmd = cmd + " " + " ".join(sys.argv[1:])
    shell_run(cmd)


def requirements():
    os.system("poetry export -f requirements.txt --output requirements.txt")


def createsuperuser():
    shell_run("python manage.py createsuperuser")


def collectstatic():
    shell_run("python manage.py collectstatic")


def djangoshell():
    shell_run("python manage.py shell")


def dbshell():
    cmd = "python manage.py dbshell"
    if len(sys.argv) > 1:
        cmd = cmd + f" '{sys.argv[1]}'"
    shell_run(cmd)


def command():
    cmd = "python manage.py"
    if len(sys.argv) > 1:
        cmd = cmd + " " + " ".join(sys.argv[1:])
    shell_run(cmd)


def start():
    migrate()
    runserver()


def migrate_remove():
    shell_run(
        'find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./.venv/*" -delete'
    )
    shell_run("rm -f ./db.sqlite3")
