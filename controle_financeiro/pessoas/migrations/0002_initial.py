# Generated by Django 3.2 on 2021-04-27 01:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pessoas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoa',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pessoa', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='juridica',
            name='pessoa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='juridica', to='pessoas.pessoa'),
        ),
        migrations.AddField(
            model_name='fisica',
            name='pessoa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fisica', to='pessoas.pessoa'),
        ),
        migrations.AddField(
            model_name='contato',
            name='pessoa',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contato', to='pessoas.pessoa'),
        ),
    ]
