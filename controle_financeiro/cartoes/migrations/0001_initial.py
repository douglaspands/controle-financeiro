# Generated by Django 3.1.7 on 2021-03-31 22:31

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
                ('titulo', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('limite', models.DecimalField(decimal_places=2, max_digits=9)),
                ('dia_fechamento', models.IntegerField()),
                ('carteira', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carteiras.carteira')),
            ],
            options={
                'ordering': ['titulo'],
            },
        ),
    ]
