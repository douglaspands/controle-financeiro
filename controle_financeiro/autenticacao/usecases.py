from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from pessoas.models import Pessoa, Fisica, Contato
from usuarios.models import Usuario

from .forms import RegistroForm


def registrar_usuario_pessoa_fisica(form: RegistroForm):
    """Registrar novo usuario pessoa fisica.

    Args:
        form (RegistroForm): Form de registro de usuario

    Raises:
        error: Em caso de erro em algum etapa, será emitido um Exception e será feito roolback do banco de dados.
    """

    _form = form.cleaned_data

    try:
        usuario = Usuario.objects.create(
            username=_form["username"],
            password=make_password(_form["password1"]),
        )

        grupo, foi_criado = Group.objects.get_or_create(name=Usuario.GRUPO_CONSUMIDOR)
        grupo.user_set.add(usuario)
        grupo.save()

        pessoa = Pessoa.objects.create(tipo=Pessoa.PESSOA_FISICA, usuario=usuario)

        Fisica.objects.create(
            nome=_form["first_name"], sobrenome=_form["last_name"], pessoa=pessoa
        )

        Contato.objects.create(email=_form["email"], pessoa=pessoa)

    except Exception as error:
        usuario.delete()
        raise error
