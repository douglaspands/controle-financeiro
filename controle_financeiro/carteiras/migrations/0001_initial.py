# Generated by Django 3.2 on 2021-04-27 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carteira',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='CentroCusto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('tipo', models.IntegerField(choices=[(1, 'Conta'), (2, 'Cartão')])),
                ('carteira', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='centro_custos', to='carteiras.carteira')),
            ],
        ),
    ]
