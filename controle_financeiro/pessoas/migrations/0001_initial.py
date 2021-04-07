# Generated by Django 3.1.7 on 2021-04-07 01:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fisica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=100)),
                ('sobrenome', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Juridica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=200)),
                ('nome_fantasia', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Pessoa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('tipo', models.CharField(choices=[('F', 'Pessoa Fisica'), ('J', 'Pessoa Juridica')], max_length=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Telefone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('tipo', models.CharField(choices=[('F', 'Telefone Fixo'), ('M', 'Telefone Móvel')], max_length=1)),
                ('numero', models.CharField(max_length=15)),
                ('contato', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='telefones', to='pessoas.contato')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]