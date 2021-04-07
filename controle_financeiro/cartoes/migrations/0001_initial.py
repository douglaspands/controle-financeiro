# Generated by Django 3.1.7 on 2021-04-07 01:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carteiras', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cartao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('limite', models.DecimalField(decimal_places=2, max_digits=11)),
                ('dia_fechamento', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(25), django.core.validators.MinValueValidator(1)])),
                ('pode_parcelar', models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')])),
                ('porta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cartao', to='carteiras.porta')),
            ],
            options={
                'ordering': ['nome'],
            },
        ),
        migrations.AddIndex(
            model_name='cartao',
            index=models.Index(fields=['slug'], name='cartoes_car_slug_d6992e_idx'),
        ),
    ]
